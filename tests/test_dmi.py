from datetime import date

from ixhardware import DMIInfo, DMIParser


def test__missing():
    assert DMIParser().parse("") == DMIInfo(
        bios_release_date=None,
        ecc_memory=False,
        baseboard_manufacturer="",
        baseboard_product_name="",
        system_manufacturer="",
        system_product_name="",
        system_serial_number="",
        system_version="",
        has_ipmi=False,
    )


full_dmi = """
# dmidecode 3.3
Getting SMBIOS data from sysfs.
SMBIOS 3.2.1 present.

Handle 0x0000, DMI type 0, 26 bytes
BIOS Information
        Vendor: American Megatrends Inc.
        Version: 3.3aV3
        Release Date: 12/03/2020
        Address: 0xF0000
        Runtime Size: 64 kB
        ROM Size: 32 MB
        Characteristics:
                PCI is supported
                BIOS is upgradeable
                BIOS shadowing is allowed
                Boot from CD is supported
                Selectable boot is supported
                BIOS ROM is socketed
                EDD is supported
                5.25"/1.2 MB floppy services are supported (int 13h)
                3.5"/720 kB floppy services are supported (int 13h)
                3.5"/2.88 MB floppy services are supported (int 13h)
                Print screen service is supported (int 5h)
                Serial services are supported (int 14h)
                Printer services are supported (int 17h)
                ACPI is supported
                USB legacy is supported
                BIOS boot specification is supported
                Targeted content distribution is supported
                UEFI is supported
        BIOS Revision: 5.14

Handle 0x0001, DMI type 1, 27 bytes
System Information
        Manufacturer: iXsystems
        Product Name: TRUENAS-M60
        Version: 0123456789
        Serial Number: A1-111111
        UUID: 00000000-0000-0000-0000-3cecef5ee7d6
        Wake-up Type: Power Switch
        SKU Number: To be filled by O.E.M.
        Family: To be filled by O.E.M.

Handle 0x0002, DMI type 2, 15 bytes
Base Board Information
        Manufacturer: Supermicro
        Product Name: X11SPH-nCTPF
        Version: 1.01
        Serial Number: 0000000000000
        Asset Tag: To be filled by O.E.M.
        Features:
                Board is a hosting board
                Board is replaceable
        Location In Chassis: To be filled by O.E.M.
        Chassis Handle: 0x0003
        Type: Motherboard
        Contained Object Handles: 0

Handle 0x0014, DMI type 38, 18 bytes
IPMI Device Information
        Interface Type: KCS (Keyboard Control Style)
        Specification Version: 2.0
        I2C Slave Address: 0x10
        NV Storage Device: Not Present
        Base Address: 0x0000000000000CA2 (I/O)
        Register Spacing: Successive Byte Boundaries

Handle 0x0024, DMI type 16, 23 bytes
Physical Memory Array
        Location: System Board Or Motherboard
        Use: System Memory
        Error Correction Type: Single-bit ECC
        Maximum Capacity: 2304 GB
        Error Information Handle: Not Provided
        Number Of Devices: 4

Handle 0x002C, DMI type 16, 23 bytes
Physical Memory Array
        Location: System Board Or Motherboard
        Use: System Memory
        Error Correction Type: Single-bit ECC
        Maximum Capacity: 2304 GB
        Error Information Handle: Not Provided
        Number Of Devices: 4

"""


def test__full():
    assert DMIParser().parse(full_dmi) == DMIInfo(
        bios_release_date=date(2020, 12, 3),
        ecc_memory=True,
        baseboard_manufacturer="Supermicro",
        baseboard_product_name="X11SPH-nCTPF",
        system_manufacturer="iXsystems",
        system_product_name="TRUENAS-M60",
        system_serial_number="A1-111111",
        system_version="0123456789",
        has_ipmi=True,
    )


double_colon_dmi = """
# dmidecode 3.3
Getting SMBIOS data from sysfs.
SMBIOS 2.7 present.Handle 0x0001, DMI type 1, 27 bytes
System Information
        Manufacturer: Supermicro
        Product Name: X9DRi-LN4+/X9DR3-LN4+
        Version: 0123456789
        Serial Number: 0123456789
        UUID: 00000000-0000-0000-0000-002590f3967a
        Wake-up Type: Power Switch
        SKU Number: To be filled by O.E.M.
        Family: To be filled by O.E.M.Handle 0x0002, DMI type 2, 15 bytes
Base Board Information
        Manufacturer: Supermicro
        Product Name: X9DRi-LN4+/X9DR3-LN4+
        Version: REV:1.20A
        Serial Number: FAKE
        Asset Tag: To be filled by O.E.M.
        Features:
                Board is a hosting board
                Board is replaceable
        Location In Chassis: To be filled by O.E.M.
        Chassis Handle: 0x0003
        Type: Motherboard
        Contained Object Handles: 0Handle 0x002F, DMI type 16, 23 bytes
Physical Memory Array
        Location: System Board Or Motherboard
        Use: System Memory
        Error Correction Type: Multi-bit ECC
        Maximum Capacity: 768 GB
        Error Information Handle: Not Provided
        Number Of Devices: 12Handle 0x0049, DMI type 16, 23 bytes
Physical Memory Array
        Location: System Board Or Motherboard
        Use: System Memory
        Error Correction Type: Multi-bit ECC
        Maximum Capacity: 768 GB
        Error Information Handle: Not Provided
        Number Of Devices: 12
"""


def test__double_colon():
    assert DMIParser().parse(double_colon_dmi) == DMIInfo(
        bios_release_date=None,
        ecc_memory=True,
        baseboard_manufacturer="Supermicro",
        baseboard_product_name="X9DRi-LN4+/X9DR3-LN4+",
        system_manufacturer="Supermicro",
        system_product_name="X9DRi-LN4+/X9DR3-LN4+",
        system_serial_number="0123456789",
        system_version="0123456789",
        has_ipmi=False,
    )


missing_dmi_type1 = """
# dmidecode 3.3
Getting SMBIOS data from sysfs.
SMBIOS 2.8 present.

Handle 0x0002, DMI type 2, 15 bytes
Base Board Information
        Manufacturer: Supermicro
        Product Name: X11SPH-nCTPF
        Version: 1.01
        Serial Number: 0000000000000
        Asset Tag: To be filled by O.E.M.
        Features:
                Board is a hosting board
                Board is replaceable
        Location In Chassis: To be filled by O.E.M.
        Chassis Handle: 0x0003
        Type: Motherboard
        Contained Object Handles: 0

Handle 0x1000, DMI type 16, 23 bytes
Physical Memory Array
        Location: Other
        Use: System Memory
        Error Correction Type: Multi-bit ECC
        Maximum Capacity: 8 GB
        Error Information Handle: Not Provided
        Number Of Devices: 1

"""


def test__missing_dmi_type1():
    assert DMIParser().parse(missing_dmi_type1) == DMIInfo(
        bios_release_date=None,
        ecc_memory=True,
        baseboard_manufacturer="Supermicro",
        baseboard_product_name="X11SPH-nCTPF",
        system_manufacturer="",
        system_product_name="",
        system_serial_number="",
        system_version="",
        has_ipmi=False,
    )


missing_dmi_type2 = """
# dmidecode 3.3
Getting SMBIOS data from sysfs.
SMBIOS 2.8 present.

Handle 0x0100, DMI type 1, 27 bytes
System Information
        Manufacturer: QEMU
        Product Name: Standard PC (Q35 + ICH9, 2009)
        Version: pc-q35-5.2
        Serial Number: Not Specified
        UUID: 236ce080-e87b-4d21-b9dd-3e43b8fb58dd
        Wake-up Type: Power Switch
        SKU Number: Not Specified
        Family: Not Specified

Handle 0x1000, DMI type 16, 23 bytes
Physical Memory Array
        Location: Other
        Use: System Memory
        Error Correction Type: Multi-bit ECC
        Maximum Capacity: 8 GB
        Error Information Handle: Not Provided
        Number Of Devices: 1

"""


def test__missing_dmi_type2():
    assert DMIParser().parse(missing_dmi_type2) == DMIInfo(
        bios_release_date=None,
        ecc_memory=True,
        baseboard_manufacturer="",
        baseboard_product_name="",
        system_manufacturer="QEMU",
        system_product_name="Standard PC (Q35 + ICH9, 2009)",
        system_serial_number="Not Specified",
        system_version="pc-q35-5.2",
        has_ipmi=False,
    )


missing_dmi_type16 = """
# dmidecode 3.3
Getting SMBIOS data from sysfs.
SMBIOS 2.8 present.

Handle 0x0100, DMI type 1, 27 bytes
System Information
        Manufacturer: QEMU
        Product Name: Standard PC (Q35 + ICH9, 2009)
        Version: pc-q35-5.2
        Serial Number: Not Specified
        UUID: 236ce080-e87b-4d21-b9dd-3e43b8fb58dd
        Wake-up Type: Power Switch
        SKU Number: Not Specified
        Family: Not Specified

Handle 0x0002, DMI type 2, 15 bytes
Base Board Information
        Manufacturer: Supermicro
        Product Name: X11SPH-nCTPF
        Version: 1.01
        Serial Number: 0000000000000
        Asset Tag: To be filled by O.E.M.
        Features:
                Board is a hosting board
                Board is replaceable
        Location In Chassis: To be filled by O.E.M.
        Chassis Handle: 0x0003
        Type: Motherboard
        Contained Object Handles: 0

"""


def test__missing_dmi_type16():
    assert DMIParser().parse(missing_dmi_type16) == DMIInfo(
        bios_release_date=None,
        ecc_memory=False,
        baseboard_manufacturer="Supermicro",
        baseboard_product_name="X11SPH-nCTPF",
        system_manufacturer="QEMU",
        system_product_name="Standard PC (Q35 + ICH9, 2009)",
        system_serial_number="Not Specified",
        system_version="pc-q35-5.2",
        has_ipmi=False,
    )


missing_dmi_type38 = """
# dmidecode 3.3
Getting SMBIOS data from sysfs.
SMBIOS 3.2.1 present.

Handle 0x0000, DMI type 0, 26 bytes
BIOS Information
        Vendor: American Megatrends Inc.
        Version: 3.3aV3
        Release Date: 12/03/2020
        Address: 0xF0000
        Runtime Size: 64 kB
        ROM Size: 32 MB
        Characteristics:
                PCI is supported
                BIOS is upgradeable
                BIOS shadowing is allowed
                Boot from CD is supported
                Selectable boot is supported
                BIOS ROM is socketed
                EDD is supported
                5.25"/1.2 MB floppy services are supported (int 13h)
                3.5"/720 kB floppy services are supported (int 13h)
                3.5"/2.88 MB floppy services are supported (int 13h)
                Print screen service is supported (int 5h)
                Serial services are supported (int 14h)
                Printer services are supported (int 17h)
                ACPI is supported
                USB legacy is supported
                BIOS boot specification is supported
                Targeted content distribution is supported
                UEFI is supported
        BIOS Revision: 5.14

Handle 0x0001, DMI type 1, 27 bytes
System Information
        Manufacturer: iXsystems
        Product Name: TRUENAS-M60
        Version: 0123456789
        Serial Number: A1-111111
        UUID: 00000000-0000-0000-0000-3cecef5ee7d6
        Wake-up Type: Power Switch
        SKU Number: To be filled by O.E.M.
        Family: To be filled by O.E.M.

Handle 0x0002, DMI type 2, 15 bytes
Base Board Information
        Manufacturer: Supermicro
        Product Name: X11SPH-nCTPF
        Version: 1.01
        Serial Number: 0000000000000
        Asset Tag: To be filled by O.E.M.
        Features:
                Board is a hosting board
                Board is replaceable
        Location In Chassis: To be filled by O.E.M.
        Chassis Handle: 0x0003
        Type: Motherboard
        Contained Object Handles: 0

Handle 0x0024, DMI type 16, 23 bytes
Physical Memory Array
        Location: System Board Or Motherboard
        Use: System Memory
        Error Correction Type: Single-bit ECC
        Maximum Capacity: 2304 GB
        Error Information Handle: Not Provided
        Number Of Devices: 4

Handle 0x002C, DMI type 16, 23 bytes
Physical Memory Array
        Location: System Board Or Motherboard
        Use: System Memory
        Error Correction Type: Single-bit ECC
        Maximum Capacity: 2304 GB
        Error Information Handle: Not Provided
        Number Of Devices: 4

"""


def test__missing_dmi_type38():
    assert DMIParser().parse(missing_dmi_type38) == DMIInfo(
        bios_release_date=date(2020, 12, 3),
        ecc_memory=True,
        baseboard_manufacturer="Supermicro",
        baseboard_product_name="X11SPH-nCTPF",
        system_manufacturer="iXsystems",
        system_product_name="TRUENAS-M60",
        system_serial_number="A1-111111",
        system_version="0123456789",
        has_ipmi=False,
    )
