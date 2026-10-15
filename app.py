"""Streamlit front end to the complete AI pipeline."""
import pandas as pd
import streamlit as st
from pipeline import read_feedback, clean_feedback, analyze_dataframe, get_client, to_excel_bytes

st.set_page_config(page_title='AI 客戶回饋分析', page_icon='📊', layout='wide')
st.title('📊 AI 客戶回饋自動化分析系統')
st.caption('Excel 資料清理 → LLM 情緒分類與摘要 → 結果驗證 → Excel 匯出')
st.info('此工具會將客戶回饋文字傳送至 OpenAI API。請使用虛構或已獲授權且符合隱私要求的資料。')
upload = st.file_uploader('上傳 .xlsx 或 .csv（需含 feedback_id、feedback）', type=['xlsx','csv'])
model = st.text_input('模型名稱', value='gemini-3.5-flash-lite')

if upload is not None:
    try:
        df = read_feedback(upload)
        cleaned, clean_stats = clean_feedback(df)
        c1,c2,c3 = st.columns(3)
        c1.metric('原始筆數', clean_stats['input_rows'])
        c2.metric('空白移除', clean_stats['blank_removed'])
        c3.metric('重複移除', clean_stats['duplicate_removed'])
        st.subheader('資料預覽')
        st.dataframe(cleaned, use_container_width=True)
        st.download_button('先下載清理資料', to_excel_bytes(cleaned), 'cleaned_feedback.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        if cleaned.empty:
            st.warning('清理後沒有可分析的資料。')
        elif st.button('開始 AI 分析', type='primary'):
            try:
                client = get_client()
                bar = st.progress(0)
                with st.spinner('正在分析，請勿關閉頁面…'):
                    output, stats = analyze_dataframe(
                        cleaned, client=client, model=model.strip(),
                        progress=lambda current,total: bar.progress(current / total))
                st.session_state['results'] = output
                st.session_state['stats'] = stats
                st.session_state['upload_name'] = upload.name
            except Exception as exc:
                st.error(f'分析未能啟動：{type(exc).__name__}: {exc}')
        if st.session_state.get('upload_name') == upload.name and 'results' in st.session_state:
            output = st.session_state['results']
            stats = st.session_state['stats']
            st.subheader('分析結果')
            a,b,c = st.columns(3)
            a.metric('處理筆數',stats['processed'])
            b.metric('成功',stats['success'])
            c.metric('失敗',stats['failed'])
            st.dataframe(output, use_container_width=True)
            if stats['sentiment_counts']:
                st.bar_chart(pd.Series(stats['sentiment_counts']))
            st.download_button('下載 AI 分析結果', to_excel_bytes(output), 'feedback_ai_results.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except ValueError as exc:
        st.error(str(exc))
