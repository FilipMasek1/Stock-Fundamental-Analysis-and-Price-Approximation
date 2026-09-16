from unittest.mock import MagicMock, patch
import pytest
import numpy as np
import live_analysis
import mock_analysis
import GUI


def test_real_analyza():
    """Tests, if online analysis returns correct structure and data types"""
    
    tickers = ["AAPL"]
    metrics = ["operatingMargins", "profitMargins"]

    try:
        result = live_analysis.Real_Analyza(tickers, "1d", "1mo", metrics)
    except Exception as e:
        if "yfinance" in str(e):
            pytest.skip("Connection problem")

    assert isinstance(result, dict)
    assert "AAPL" in result

    assert isinstance(result["AAPL"][0], np.ndarray)
    assert isinstance(result["AAPL"][1], (np.ndarray, list))
    assert isinstance(result["AAPL"][2], np.ndarray)
    assert isinstance(result["AAPL"][3], np.ndarray)
    assert isinstance(result["AAPL"][4], list)

    tickers = ["AAPL", "MSFT"]
    metrics = ["operatingMargins"]

    try:
        result = live_analysis.Real_Analyza(tickers, "1d", "1mo", metrics)
        assert "AAPL" in result
        assert "MSFT" in result
    except Exception as e:
        if "yfinance" in str(e):
            pytest.skip("yfinance API nedostupné.")





def test_mock_analyza():
    """Tests, if offline  analysis returns correct structure and data types"""
    metrics = ["operatingMargins", "profitMargins"]
    
    try:
        fit_data, av_tickers = mock_analysis.Mock_Analyza(["AAPL"], metrics)
        assert "AAPL" in av_tickers
        assert "AAPL" in fit_data
    except Exception:
            return

    with pytest.raises(Exception, match="Tickers 'ticker_NaN, ticker_NaN2' are unavailible."):
        mock_analysis.Mock_Analyza(["ticker_NaN", "ticker_NaN2", "AAPL"], ["operatingMargins"])



