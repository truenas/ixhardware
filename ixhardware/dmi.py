from dataclasses import dataclass
from datetime import date, datetime
from functools import cache
import logging
import subprocess

logger = logging.getLogger(__name__)

__all__ = ["DMIInfo", "DMIParser", "parse_dmi"]


@dataclass(slots=True, frozen=True, kw_only=True)
class DMIInfo:
    bios_release_date: date | None = None
    ecc_memory: bool = False
    baseboard_manufacturer: str = ""
    baseboard_product_name: str = ""
    system_manufacturer: str = ""
    system_product_name: str = ""
    system_serial_number: str = ""
    system_version: str = ""
    has_ipmi: bool = False


class DMIParser:
    command = ["dmidecode", "-t", "0,1,2,16,38"]

    def parse(self, output: str) -> DMIInfo:
        return self._parse_dmi(output.splitlines())

    def _parse_dmi(self, lines: list[str]) -> DMIInfo:
        info = dict()
        _type = None
        for line in lines:
            if "DMI type 0," in line:
                _type = "RELEASE_DATE"
            if "DMI type 1," in line:
                _type = "SYSINFO"
            if "DMI type 2," in line:
                _type = "BBINFO"
            if "DMI type 38," in line:
                _type = "IPMI"

            if not line or ":" not in line:
                # "sections" are separated by the category name and then
                # a newline so ignore those lines
                continue

            sect, val = [i.strip() for i in line.split(":", 1)]
            if sect == "Release Date":
                info["bios_release_date"] = self._parse_bios_release_date(val)
            elif sect == "Manufacturer":
                if _type == "SYSINFO":
                    info["system_manufacturer"] = val
                else:
                    info["baseboard_manufacturer"] = val
            elif sect == "Product Name":
                if _type == "SYSINFO":
                    info["system_product_name"] = val
                else:
                    info["baseboard_product_name"] = val
            elif sect == "Serial Number" and _type == "SYSINFO":
                info["system_serial_number"] = val
            elif sect == "Version" and _type == "SYSINFO":
                info["system_version"] = val
            elif sect == "I2C Slave Address":
                info["has_ipmi"] = True
            elif sect == "Error Correction Type":
                info["ecc_memory"] = "ECC" in val
                # we break the for loop here since "16" is the last section
                # that gets processed
                break
        return DMIInfo(**info)

    def _parse_bios_release_date(self, string):
        parts = string.strip().split("/")
        if len(parts) < 3:
            # Don"t know what the BIOS is reporting so assume it"s invalid
            return

        # Give the best effort to convert to a date object.
        # Searched hundreds of debugs that have been provided
        # via end-users and 99% all reported the same date
        # format, however, there are a couple that had a
        # 2 digit year instead of a 4 digit year...gross
        formatter = "%m/%d/%Y" if len(parts[-1]) == 4 else "%m/%d/%y"
        try:
            return datetime.strptime(string, formatter).date()
        except Exception as e:
            logger.warning(
                f"Failed to format BIOS release date to datetime object: {e!r}"
            )


@cache
def parse_dmi() -> DMIInfo:
    return DMIParser().parse(
        subprocess.run(
            DMIParser.command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            encoding="utf-8",
            errors="ignore",
        ).stdout
    )
