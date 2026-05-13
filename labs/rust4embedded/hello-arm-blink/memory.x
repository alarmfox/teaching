ENTRY(_init)

MEMORY
{
  FLASH : ORIGIN = 0x08000000, LENGTH = 256K
  RAM   : ORIGIN = 0x20000000, LENGTH = 40K
}

_stack_size = 128;
_stack_top  = ORIGIN(RAM) + LENGTH(RAM);

SECTIONS {
  /* 1. Place the vector table at the very beginning of FLASH */
  .vector_table : {
    KEEP(*(.vector_table));
  } > FLASH

  /* 2. Place the executable code into FLASH right after the vector table */
  .text : {
    *(.text .text.*);
  } > FLASH

  /* Any data/bss sections would be added down here later and mapped to RAM */
}
