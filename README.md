
# [LR11xx](https://www.semtech.com/products/wireless-rf/lora-edge) SPI command parser for [Saleae](https://www.saleae.com/)
For LR1110, LR1120 and LR1121 transceiver chips.
  
## hookup
SPI pins required: SCLK, MISO, MOSI, nSS, and highly suggested to connect the interrupt DIO9 (or DIO11) pin and BUSY pin.  

As an extra addition, if you desire to know the operating mode time durations, you can simultaneously use the [LR11xx operating mode](https://github.com/dudmuck/lr11xx_mode) parser for Saleae.

## implementation
this python code mirrors LR11xx driver https://github.com/Lora-net/SWDR001

## Modem-E
`lr_modem_e.py` decodes the LR1121 Modem-E command groups (0x0600 BSP, 0x0601 MODEM,
0x0602 LORAWAN, 0x0603 RELAY), mirroring https://github.com/Lora-net/lr1121_modemE_driver
Under Modem-E firmware every response — System (0x01xx) and RadioCtrl (0x02xx) groups
included — is framed `[RC, payload, CRC]` (Modem-E Reference Manual Tables 2-4/2-5), not
`[stat1, data]` as with transceiver firmware. The analyzer's **firmware** setting selects
which framing to parse:
* `auto` (default) — assume transceiver until Modem-E traffic (an 0x06xx command or a
  self-identifying RC read-back like `00 52`) is seen, then switch.
* `modem-e` — Modem-E framing from the first frame (use this when the capture contains
  only System/RadioCtrl commands, which look identical in both firmwares).
* `transceiver` — never apply Modem-E framing.

When run outside Logic 2 (e.g. a standalone harness that instantiates the HLA without
settings), the mode can be forced with the `LR11XX_FIRMWARE` environment variable:
`LR11XX_FIRMWARE=modem-e python3 spi_hla.py ...`

With Modem-E framing active: responses are decoded with their RC byte, the trailing CRC
(poly 0x65, init 0xFF — modem_e_modem_compute_crc) is validated (`[crc BAD]` on mismatch),
error responses (`[RC, CRC]` with no payload) are reported as `<Cmd> RC=...`, command
frames have their trailing CRC checked (`[cmd crc BAD]`), and the 2-byte RC read-back the
HAL clocks after each write command (MOSI `00 00`, MISO `[RC, CRC]`, see
modem_e_hal_impl.c in ModemE_application_examples) is decoded as `ModemE RC=...`
(all-zero MISO reported as `no response`). A command frame arriving while a response was
expected is treated as a command retry, matching the reference HAL's behavior.
