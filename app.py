import streamlit as st
import json
from generate_qa import create_qa # 先ほど作ったファイルを読み込む

st.set_page_config(page_title="QA自動生成システム", layout="wide")
st.title("📝 講義内容QA 自動生成システム (MVP版)")

st.info("左のサイドバーで設定を入力し、講義内容を貼り付けて「QA生成」ボタンを押してください。")

# --- サイドバーに入力項目をまとめる ---
with st.sidebar:
    st.header("設定")
    num_q = st.slider("生成する問題数", 1, 10, 5)
    difficulty_map = {"易しい": "易", "普通": "中", "難しい": "難"}
    selected_difficulty_label = st.radio("難易度", list(difficulty_map.keys()))
    difficulty_code = difficulty_map[selected_difficulty_label]

# --- メイン画面 ---
lecture_input = st.text_area("ここに講義内容のテキストを貼り付けてください", height=250)

if st.button("QAを生成する"):
    if not lecture_input:
        st.warning("講義内容を入力してください。")
    else:
        with st.spinner("QAを生成中です..."):
            # QA生成関数を呼び出し
            generated_json_str = create_qa(lecture_input, num_q, difficulty_code)
            
            try:
                # 結果を画面に表示
                qa_data = json.loads(generated_json_str)
                st.success("QAが生成されました！")
                
                for qa in qa_data["qa_set"]:
                    st.subheader(f"問{qa['question_id']} ({qa['difficulty']}) - {qa['type']}")
                    st.write(qa['question_text'])
                    if qa['type'] == '一択選択式':
                        st.radio("選択肢", qa['options'], key=f"q{qa['question_id']}", label_visibility="collapsed")
                    
                    with st.expander("答えと解説を見る"):
                        st.markdown(f"**正解:** {qa['answer']}")
                        st.markdown(f"**解説:** {qa['explanation']}")

            except Exception as e:
                st.error("エラー：結果の解析に失敗しました。もう一度試してください。")
                st.code(generated_json_str) # エラーの場合は生の出力を表示