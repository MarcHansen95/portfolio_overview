import pandas as pd
from src.data import loader as loader_module


def test_save_portfolio_data_recalculates_values(tmp_path, monkeypatch):
    data_file = tmp_path / "portfolio_data.xlsx"
    monkeypatch.setattr(loader_module, "DATA_FILE", str(data_file))

    df = pd.DataFrame(
        [
            {
                "Mapped_Security": "Test Holding",
                "Antal": 10,
                "Price": 100,
                "Value_DKK": 1,
                "Return_Percent": 5,
                "Weight": 1,
            }
        ]
    )

    loader_module.DataLoader.save_portfolio_data(df)

    reloaded = pd.read_excel(data_file)

    assert reloaded.loc[0, "Value_DKK"] == 1000
    assert reloaded.loc[0, "Return_DKK"] == 50
    assert reloaded.loc[0, "Weight"] == 100.0
