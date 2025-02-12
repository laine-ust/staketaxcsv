

from terra.col5.contracts.config import CONTRACTS
from terra import util_terra
from common.make_tx import make_transfer_in_tx, make_unknown_tx, make_transfer_out_tx


def handle_wormhole(exporter, elem, txinfo):
    txid = txinfo.txid
    COMMENT = "bridge wormhole"

    for msg in txinfo.msgs:
        transfers_in, transfers_out = msg.transfers

        # Check native coins
        if len(transfers_in) == 1 and len(transfers_out) == 0:
            amount, currency = transfers_in[0]
            row = make_transfer_in_tx(txinfo, amount, currency)
            row.comment = COMMENT
            return [row]
        elif len(transfers_out) == 1 and len(transfers_in) == 0:
            amount, currency = transfers_out[0]
            row = make_transfer_out_tx(txinfo, amount, currency)
            row.comment = COMMENT
            return [row]

        # Check other coins
        for action in msg.actions:
            if action["action"] == "complete_transfer_wrapped":
                amount_string = action["amount"]
                currency_address = action["contract"]

                currency = util_terra._lookup_address(currency_address, txid)
                amount = util_terra._float_amount(amount_string, currency)
                row = make_transfer_in_tx(txinfo, amount, currency)
                row.comment = COMMENT
                return [row]

    row = make_unknown_tx(txinfo)
    return [row]


# Wormhole Contracts
CONTRACTS["terra10nmmwe8r3g99a9newtqa7a75xfgs2e8z87r2sf"] = handle_wormhole
