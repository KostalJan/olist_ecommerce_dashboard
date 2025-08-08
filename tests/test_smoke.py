from src.olist_dash.io.load import read_orders

def test_orders_loadable():
    df = read_orders()
    assert not df.empty
    assert "order_status" in df.columns
