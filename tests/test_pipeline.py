import io
import pandas as pd
import pytest
from pipeline import clean_feedback, read_feedback, validate_result, analyze_dataframe, to_excel_bytes


def test_cleaning():
    df = pd.DataFrame({'feedback_id':['1','2','3','4'], 'feedback':[' 好評 ','好評','', '出貨慢']})
    cleaned, s = clean_feedback(df)
    assert s == {'input_rows':4,'blank_removed':1,'duplicate_removed':1,'cleaned_rows':2}
    assert cleaned['feedback'].tolist() == ['好評','出貨慢']


def test_missing_column():
    with pytest.raises(ValueError, match='缺少必要欄位'):
        clean_feedback(pd.DataFrame({'feedback_id':['1']}))


def test_invalid_llm_result():
    with pytest.raises(ValueError):
        validate_result({'sentiment':'其他','summary':'ok'})


def test_one_failure_does_not_stop_batch():
    df = pd.DataFrame({'feedback_id':['1','2'],'feedback':['喜歡','錯誤']})
    def fake(text, **kwargs):
        if text == '錯誤':
            raise RuntimeError('mock failure')
        return {'sentiment':'正面','summary':'喜歡服務'}
    result, stats = analyze_dataframe(df, classify=fake, retries=0)
    assert stats['success'] == 1 and stats['failed'] == 1
    assert result['status'].tolist() == ['success','failed']


def test_excel_round_trip():
    df = pd.DataFrame({'feedback_id':['A1'], 'feedback':['OK']})
    data = to_excel_bytes(df)
    actual = read_feedback(io.BytesIO(data))
    assert actual.loc[0,'feedback'] == 'OK'
