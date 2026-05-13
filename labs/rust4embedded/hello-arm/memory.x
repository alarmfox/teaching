MEMORY
{
  /* Datasheet */
  RAM : ORIGIN = 0x20000000, LENGTH = 40K
}

/* We need a 128B of stack to start with. Place it at the end of memory */
_stack_size = 128;
_stack_top  = ORIGIN(RAM) + LENGTH(RAM);

SECTIONS {

  /* text region */
  .text : ALIGN(4K) {
    KEEP(*(._init));
    . = ALIGN(4K);
    *(.text .text.*);
  } > RAM
}
