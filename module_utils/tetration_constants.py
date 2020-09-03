# This file contains all the constants in use by the tetration modules

# defining tetration constants
TETRATION_API_INVENTORY_TAG = '/inventory/tags'
TETRATION_API_ROLE = '/roles'
TETRATION_API_TENANT = '/vrfs'
TETRATION_API_USER = '/users'
TETRATION_API_SENSORS = '/sensors'
TETRATION_API_INVENTORY_FILTER = '/filters/inventories'
TETRATION_API_SCOPES = '/app_scopes'
TETRATION_API_INTERFACE_INTENTS = '/inventory_config/interface_intents'
TETRATION_API_AGENT_NAT_CONFIG = '/agentnatconfig'
TETRATION_API_APPLICATIONS = '/applications'
TETRATION_API_APPLICATION_POLICIES = '/policies'
TETRATION_API_AGENT_CONFIG_PROFILES = '/inventory_config/profiles'
TETRATION_API_AGENT_CONFIG_INTENTS = '/inventory_config/intents'
TETRATION_COLUMN_NAMES = '/assets/cmdb/attributenames'
TETRATION_API_EXT_ORCHESTRATORS = '/orchestrator'
TETRATION_API_APP_SCOPE_CAPABILITIES = ['SCOPE_READ', 'SCOPE_WRITE', 'EXECUTE',
                                        'ENFORCE', 'SCOPE_OWNER', 'DEVELOPER']

TETRATION_API_SUCCESS_CODES = [200, 202]

# 422 is for the SCOPE Delete API
TETRATION_API_FAILURE_CODES_THAT_RETURN_DATA = [422]

TETRATION_PROVIDER_SPEC = {
    'server_endpoint': dict(type='str', required=True, aliases=['endpoint', 'host']),
    'api_key': dict(type='str', required=True),
    'api_secret': dict(type='str', required=True, no_log=True),
    'verify': dict(type='bool', default=False),
    'timeout': dict(type='int', default=10),
    'max_retries': dict(type='int', default=3),
    'api_version': dict(type='str', default='v1')
}

TETRATION_API_PROTOCOLS = [
    dict(name='ANY', value=""),
    dict(name='TCP', value=6),
    dict(name='UDP', value=17),
    dict(name='ICMP', value=1),
    dict(name='Other', value=0),
    dict(name='A/N', value=107),
    dict(name='AH', value=51),
    dict(name='ARGUS', value=13),
    dict(name='ARIS', value=104),
    dict(name='AX.25', value=93),
    dict(name='BBN-RCC-MON', value=10),
    dict(name='BNA', value=49),
    dict(name='BR-SAT-MON', value=76),
    dict(name='CARP', value=112),
    dict(name='CBT', value=7),
    dict(name='CFTP', value=62),
    dict(name='CHAOS', value=16),
    dict(name='CPHB', value=73),
    dict(name='CPNX', value=72),
    dict(name='CRTP', value=126),
    dict(name='CRUDP', value=127),
    dict(name='Compaq-Peer', value=110),
    dict(name='DCCP', value=33),
    dict(name='DCN-MEAS', value=19),
    dict(name='DDP', value=37),
    dict(name='DDX', value=116),
    dict(name='DGP', value=86),
    dict(name='DIVERT', value=258),
    dict(name='DSR', value=48),
    dict(name='EGP', value=8),
    dict(name='EIGRP', value=88),
    dict(name='EMCON', value=14),
    dict(name='ENCAP', value=98),
    dict(name='ESP', value=50),
    dict(name='ETHERIP', value=97),
    dict(name='FC', value=133),
    dict(name='FIRE', value=125),
    dict(name='GGP', value=3),
    dict(name='GMTP', value=100),
    dict(name='GRE', value=47),
    dict(name='HIP', value=139),
    dict(name='HMP', value=20),
    dict(name='I-NLSP', value=52),
    dict(name='IATP', value=117),
    dict(name='IDPR', value=35),
    dict(name='IDPR-CMTP', value=38),
    dict(name='IDRP', value=45),
    dict(name='IFMP', value=101),
    dict(name='IGMP', value=2),
    dict(name='IGP', value=9),
    dict(name='IL', value=40),
    dict(name='IP-ENCAP', value=4),
    dict(name='IPCV', value=71),
    dict(name='IPComp', value=108),
    dict(name='IPIP', value=94),
    dict(name='IPLT', value=129),
    dict(name='IPPC', value=67),
    dict(name='IPV6', value=41),
    dict(name='IPV6-FRAG', value=44),
    dict(name='IPV6-ICMP', value=58),
    dict(name='IPV6-NONXT', value=59),
    dict(name='IPV6-OPTS', value=60),
    dict(name='IPV6-ROUTE', value=43),
    dict(name='IPX-in-IP', value=111),
    dict(name='IRTP', value=28),
    dict(name='ISIS', value=124),
    dict(name='ISO-IP', value=80),
    dict(name='ISO-TP4', value=29),
    dict(name='KRYPTOLAN', value=65),
    dict(name='L2TP', value=115),
    dict(name='LARP', value=91),
    dict(name='LEAF-1', value=25),
    dict(name='LEAF-2', value=26),
    dict(name='MANET', value=138),
    dict(name='MERIT-INP', value=32),
    dict(name='MFE-NSP', value=31),
    dict(name='MICP', value=95),
    dict(name='MOBILE', value=55),
    dict(name='MPLS-IN-IP', value=137),
    dict(name='MTP', value=92),
    dict(name='MUX', value=18),
    dict(name='Mobility-Header', value=135),
    dict(name='NARP', value=54),
    dict(name='NETBLT', value=30),
    dict(name='NSFNET-IGP', value=85),
    dict(name='NVP-II', value=11),
    dict(name='OSPFIGP', value=89),
    dict(name='PFSYNC', value=240),
    dict(name='PGM', value=113),
    dict(name='PIM', value=103),
    dict(name='PIPE', value=131),
    dict(name='PNNI', value=102),
    dict(name='PRM', value=21),
    dict(name='PTP', value=123),
    dict(name='PUP', value=12),
    dict(name='PVP', value=75),
    dict(name='QNX', value=106),
    dict(name='RDP', value=27),
    dict(name='ROHC', value=142),
    dict(name='RSVP', value=46),
    dict(name='RSVP-E2E-IGNORE', value=134),
    dict(name='RVD', value=66),
    dict(name='SAT-EXPAK', value=64),
    dict(name='SAT-MON', value=69),
    dict(name='SCC-SP', value=96),
    dict(name='SCPS', value=105),
    dict(name='SCTP', value=132),
    dict(name='SDRP', value=42),
    dict(name='SECURE-VMTP', value=82),
    dict(name='SHIM6', value=140),
    dict(name='SKIP', value=57),
    dict(name='SM', value=122),
    dict(name='SMP', value=121),
    dict(name='SNP', value=109),
    dict(name='SPS', value=130),
    dict(name='SRP', value=119),
    dict(name='SSCOPMCE', value=128),
    dict(name='ST2', value=5),
    dict(name='STP', value=118),
    dict(name='SUN-ND', value=77),
    dict(name='SWIPE', value=53),
    dict(name='Sprite-RPC', value=90),
    dict(name='TCF', value=87),
    dict(name='TLSP', value=56),
    dict(name='TP++', value=39),
    dict(name='TRUNK-1', value=23),
    dict(name='TRUNK-2', value=24),
    dict(name='TTP', value=84),
    dict(name='UDPLite', value=136),
    dict(name='UTI', value=120),
    dict(name='VINES', value=83),
    dict(name='VISA', value=70),
    dict(name='VMTP', value=81),
    dict(name='WB-EXPAK', value=79),
    dict(name='WB-MON', value=78),
    dict(name='WESP', value=141),
    dict(name='WSN', value=74),
    dict(name='XNET', value=15),
    dict(name='XNS-IDP', value=22),
    dict(name='XTP', value=36),
]
