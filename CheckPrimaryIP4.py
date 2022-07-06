from dcim.choices import DeviceStatusChoices
from dcim.models import Device
from extras.reports import Report
from ipam.choices import IPAddressStatusChoices
from virtualization.choices import VirtualMachineStatusChoices
from virtualization.models import VirtualMachine

# device / VM roles that require a primary IPv4
MANDATORY_IP4_ROLES = [
    "console-server",
    "load-balancer",
    "router",
    "switch",
    "voice-gateway",
    "wan-accelerator",
    "wireless-controller",
]


class CheckAddress(Report):
    description = (
        "For devices that require an address, check that they have a primary IPv4 set"
    )

    def has_primary_ip4(self, entity):
        return bool(entity.primary_ip4)

    def needs_ip(self, entity):
        # devices store role in the 'device_role' property
        if hasattr(entity, "device_role"):
            if entity.device_role.slug in MANDATORY_IP4_ROLES:
                return True
        # virtual machines store role in the 'role' property
        elif hasattr(entity, "role"):
            if entity.role.slug in MANDATORY_IP4_ROLES:
                return True
        return False

    def test_entity_primary_ip4(self):
        devices = Device.objects.filter(status=DeviceStatusChoices.STATUS_ACTIVE)
        vms = VirtualMachine.objects.filter(
            status=VirtualMachineStatusChoices.STATUS_ACTIVE
        )
        entities = devices + vms
        for entity in entities:
            if self.needs_ip(entity) is True and self.has_primary_ip4(entity) is False:
                self.log_failure(entity, "Missing primary IPv4 address")
            else:
                self.log_success(entity)
