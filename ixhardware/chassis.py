import typing

from pyudev import Context

from .dmi import DMIInfo

__all__ = [
    "PLATFORM_PREFIXES", "TRUENAS_UNKNOWN", "get_chassis_hardware", "TRUENAS_BHYVE", "TRUENAS_QEMU",
    "get_bhyve_hardware_and_node",
]


# We tag SMBIOS with relevant strings for each platform
# before we ship to customer. These are the various prefixes
# that represent each hardware platform.
# ("TRUENAS-X10", "TRUENAS-M50", "TRUENAS-MINI-X+", "FREENAS-MINI-X", etc)
PLATFORM_PREFIXES = (
    "TRUENAS-Z",  # z-series
    "TRUENAS-X",  # x-series
    "TRUENAS-M",  # m-series AND current mini platforms
    "TRUENAS-F",  # f-series (F60, F100, F130)
    "TRUENAS-H",  # h-series (H10, H20)
    "TRUENAS-R",  # freenas certified replacement
    "FREENAS-MINI",  # minis tagged with legacy information
)
TRUENAS_BHYVE = "BHYVE"
TRUENAS_QEMU = "IXKVM"
TRUENAS_UNKNOWN = "TRUENAS-UNKNOWN"


def get_chassis_hardware(dmi: DMIInfo):
    if dmi.system_product_name.startswith(PLATFORM_PREFIXES):
        return dmi.system_product_name

    if dmi.baseboard_product_name == "iXsystems TrueNAS X10":
        # could be that production didn"t burn in the correct x-series
        # model information so let"s check the motherboard model as a
        # last resort
        return "TRUENAS-X"

    elif dmi.system_product_name == "qemu" and dmi.system_serial_number.startswith(
        "ha"
    ) and dmi.system_serial_number.endswith(("_c1", "_c2")):
        return TRUENAS_QEMU

    elif dmi.system_product_name == "BHYVE":
        if get_bhyve_hardware_and_node()[0] == "BHYVE":
            return TRUENAS_BHYVE

    return TRUENAS_UNKNOWN


def get_bhyve_hardware_and_node() -> typing.Tuple[str, str]:
    # bhyve host configures a scsi_generic device that when sent an inquiry will
    # respond with a string that we use to determine the position of the node
    HARDWARE = NODE = "MANUAL"
    ctx = Context()
    for i in ctx.list_devices(subsystem="scsi_generic"):
        if (model := i.attributes.get("device/model")) is not None:
            model = model.decode().strip() if isinstance(model, bytes) else model.strip()
            if model == "TrueNAS_A":
                NODE = "A"
                HARDWARE = "BHYVE"
                break
            elif model == "TrueNAS_B":
                NODE = "B"
                HARDWARE = "BHYVE"
                break

    return HARDWARE, NODE
