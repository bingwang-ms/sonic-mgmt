import pytest
import logging
import ipaddress
import json
import re
import time
from tests.common.dualtor.dual_tor_mock import *
from tests.common.helpers.assertions import pytest_assert as pt_assert
from tests.common.dualtor.dual_tor_utils import rand_selected_interface, verify_upstream_traffic
from tests.common.utilities import compare_crm_facts
from tests.common.config_reload import config_reload
from tests.common.dualtor.mux_simulator_control import url, toggle_mux_simulator_to_tor
from tests.common.fixtures.ptfhost_utils import change_mac_addresses, run_garp_service, run_icmp_responder

logger = logging.getLogger(__file__)

pytestmark = [
    pytest.mark.topology('t0'),
    pytest.mark.usefixtures('apply_mock_dual_tor_tables', 'apply_mock_dual_tor_kernel_configs', 'run_garp_service', 'run_icmp_responder')
]

PAUSE_TIME = 10

def get_l2_rx_drop(host, itfs):
    """
    Return L2 rx packet drop counter for given interface
    """
    res = {}
    stdout = host.shell("portstat -j")['stdout']
    match = re.search("Last cached time was.*\n", stdout)
    if match:
        stdout = re.sub("Last cached time was.*\n", "", stdout)
    data = json.loads(stdout)
    return int(data[itfs]['RX_DRP'])


def clear_portstat(dut):
    dut.shell("portstat -c")


def is_mocked_dualtor(tbinfo):
    return 'dualtor' not in tbinfo['topo']['name']


@pytest.fixture(scope='module', autouse=True)
def test_cleanup(rand_selected_dut):
    """
    Issue a config reload at the end of module
    """
    yield
    config_reload(rand_selected_dut)


def set_mux_state(rand_selected_dut, rand_unselected_dut, tbinfo, mux_url, state, itfs):
    if is_mocked_dualtor(tbinfo):
        set_dual_tor_state_to_orchagent(rand_selected_dut, state, [itfs])
    else:
        if state == 'active':
            toggle_mux_simulator_to_tor(rand_selected_dut, mux_url, tbinfo)
        else:
            toggle_mux_simulator_to_tor(rand_unselected_dut, mux_url, tbinfo)


def test_standby_tor_upstream(rand_selected_dut, rand_unselected_dut, tbinfo, ptfadapter, rand_selected_interface, url):
    itfs, ip = rand_selected_interface
    mux_url = url(itfs)
    crm_facts0 = rand_selected_dut.get_crm_facts()
    PKT_NUM = 100
    # Step 1. Set mux state to standby and verify traffic is dropped by ACL rule and drop counters incremented
    set_mux_state(rand_selected_dut, rand_unselected_dut, tbinfo, mux_url, 'standby', itfs)
    # Wait sometime for mux toggle
    time.sleep(PAUSE_TIME)
    # Verify packets are not go up
    verify_upstream_traffic(host=rand_selected_dut,
                            ptfadapter=ptfadapter,
                            tbinfo=tbinfo,
                            itfs=itfs,
                            server_ip=ip['server_ipv4'].split('/')[0],
                            pkt_num=PKT_NUM,
                            drop=True)

    time.sleep(5)
    # Verify dropcounter is increased
    drop_counter = get_l2_rx_drop(rand_selected_dut, itfs)
    pt_assert(drop_counter >= PKT_NUM,
                "RX_DRP for {} is expected to increase by {} actually {}".format(itfs, PKT_NUM, drop_counter))

    # Step 2. Toggle mux state to active, and verify traffic is not dropped by ACL and fwd-ed to uplinks; verify CRM show and no nexthop objects are stale
    set_mux_state(rand_selected_dut, rand_unselected_dut, tbinfo, mux_url, 'active', itfs)
    # Wait sometime for mux toggle
    time.sleep(PAUSE_TIME)
    # Verify packets are not go up
    verify_upstream_traffic(host=rand_selected_dut,
                            ptfadapter=ptfadapter,
                            tbinfo=tbinfo,
                            itfs=itfs,
                            server_ip=ip['server_ipv4'].split('/')[0],
                            pkt_num=PKT_NUM,
                            drop=False)
    crm_facts1 = rand_selected_dut.get_crm_facts()
    unmatched_crm_facts = compare_crm_facts(crm_facts0, crm_facts1)
    pt_assert(len(unmatched_crm_facts)==0, 'Unmatched CRM facts: {}'.format(json.dumps(unmatched_crm_facts, indent=4)))

    # Step 3. Toggle mux state to standby, and verify traffic is dropped by ACL; verify CRM show and no nexthop objects are stale
    set_mux_state(rand_selected_dut, rand_unselected_dut, tbinfo, mux_url, 'standby', itfs)
     # Wait sometime for mux toggle
    time.sleep(PAUSE_TIME)
    # Verify packets are not go up again
    verify_upstream_traffic(host=rand_selected_dut,
                            ptfadapter=ptfadapter,
                            tbinfo=tbinfo,
                            itfs=itfs,
                            server_ip=ip['server_ipv4'].split('/')[0],
                            pkt_num=PKT_NUM,
                            drop=True)
    # Verify dropcounter is increased
    drop_counter = get_l2_rx_drop(rand_selected_dut, itfs)
    pt_assert(drop_counter >= PKT_NUM,
                "RX_DRP for {} is expected to increase by {} actually {}".format(itfs, PKT_NUM, drop_counter))
    crm_facts2 = rand_selected_dut.get_crm_facts()
    unmatched_crm_facts = compare_crm_facts(crm_facts0, crm_facts2)
    pt_assert(len(unmatched_crm_facts)==0, 'Unmatched CRM facts: {}'.format(json.dumps(unmatched_crm_facts, indent=4)))

