from dcim.choices import DeviceStatusChoices
from dcim.models import Device
from extras.reports import Report

MANDATORY_PLATFORM_ROLES = [
    "firewall",
    "load-balancer",
    "router",
    "switch",
    "voice-gateway",
    "wan-accelerator",
    "wireless-controller",
]

class CheckDevicePlatform(Report):
    description = "Find all devices without a platform value"

    def test_check_device_platform(self):
        for device in Device.objects.filter(status=DeviceStatusChoices.STATUS_ACTIVE):
            if device.device_role.slug in MANDATORY_PLATFORM_ROLES:
                if not device.platform:
                    self.log_failure(device, "Device is missing a platform (OS)")
                else:
                    self.log_success(device)
