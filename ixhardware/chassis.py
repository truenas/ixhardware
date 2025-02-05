from .dmi import DMIInfo, parse_dmi

__all__ = ["PLATFORM_PREFIXES", "TRUENAS_UNKNOWN", "get_chassis_hardware"]


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
TRUENAS_UNKNOWN = "TRUENAS-UNKNOWN"


def get_chassis_hardware(dmi: DMIInfo | None = None) -> str:
    if dmi is None:
        dmi = parse_dmi()

    if dmi.system_product_name.startswith(PLATFORM_PREFIXES):
        return dmi.system_product_name

    if dmi.baseboard_product_name == "iXsystems TrueNAS X10":
        # could be that production didn"t burn in the correct x-series
        # model information so let"s check the motherboard model as a
        # last resort
        return "TRUENAS-X"

    return TRUENAS_UNKNOWN
