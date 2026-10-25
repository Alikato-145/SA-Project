# PromptPay implementation references for Task7

Read25October2026; research only, no generated QR/payment feature claimed yet.

BOT technical supplement defines PromptPay transfer tag29/AID A000000677010111, phone subtag01 with13digits (0066 plus nine national digits), THB currency764, amount tag54, countryTH and CRCtag63. Use mobile recipient only for this delivery. [Bank of Thailand Thai QR Payment Standard, annex pp14–18](https://www.bot.or.th/content/dam/bot/documents/th/our-roles/payment-systems/about-payment-systems/ThaiQRCode_Payment_Standard.pdf).

EMVCo distinguishes QR encoding from payment-provider messaging. Generation cannot confirm actual settlement. [EMVCo QR overview](https://www.emvco.com/emv-technologies/qr-codes/).

The upstream PromptPay JS implementation uses dynamic initiation12 for an amount, includes6304 in checksum input and computes crc16xmodem with initial0xffff. Its amount API is number/toFixed(2); do not introduce floating-point payroll arithmetic to use it. Prefer tiny exact-string TLV assembly plus tested CRC, or a verified adapter retaining exact snapshot amount. Cross-check known vectors against upstream tests, and decode independently. [Author implementation](https://github.com/dtinth/promptpay-qr/blob/master/index.js), [author tests](https://github.com/dtinth/promptpay-qr/blob/master/index.test.js).

Rendering can use `qrcode` toString withSVG (or PNG dataURL); default quiet-zone margin4. No external QR-generation service should receive employee recipient/amount. [node-qrcode author docs](https://github.com/soldair/node-qrcode).

A dev-only independent decoder `jsQR` consumes RGBA Uint8ClampedArray plus width/height and returns decoded data. Browser test may draw the actual rendered QR image to same-origin canvas, read pixels and decode them; assert recipient/amount/CRC and unchanged snapshots after live phone edits. Avoid a test that only compares the payload-builder output with itself. [jsQR author docs](https://github.com/cozmo/jsQR).

Before installing dependencies, check existing packages; use only renderer and dev decoder needed. No bank API/callback, no public payload service or real transfers in tests.
