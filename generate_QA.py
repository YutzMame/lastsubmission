import os
from openai import OpenAI

# この部分を自分のAPIキーに書き換えてください
# os.environ["OPENAI_API_KEY"] = "sk-..." 
client = OpenAI()

def create_qa(lecture_text, num_questions, difficulty):
    # --- ここがAIへの命令文（プロンプト）です ---
    system_prompt = """
あなたは、講義内容から学習者の理解度を測るための問題を作成する専門家です。
以下のルールに従って、与えられた講義内容から質の高いQAセットを作成してください。

# ルール
- 質問形式は「一択選択式」「記述式」をバランス良く含めること。
- 指定された難易度（易・中・難）で問題を作成すること。
- 回答には、なぜそれが正解なのかの短い解説を必ず含めること。
- 出力は必ず指定されたJSON形式とすること。

# JSON形式の例
{
  "qa_set": [
    {
      "question_id": 1,
      "difficulty": "易",
      "type": "一択選択式",
      "question_text": "AI開発のプロセスで、最初にやるべきことは何ですか？",
      "options": ["A: モデル学習", "B: データ収集", "C: 問題設定", "D: デプロイ"],
      "answer": "C: 問題設定",
      "explanation": "どのような課題を解決したいのか、問題設定が全ての開発の出発点となります。"
    },
    {
      "question_id": 2,
      "difficulty": "中",
      "type": "記述式",
      "question_text": "「MLOps」が必要とされる背景を簡単に説明してください。",
      "answer": "モデルは一度作ったら終わりではなく、実運用では環境の変化（データやルールの変化）によって精度が劣化するため。継続的な監視・再学習・改善のループを支える仕組みとしてMLOpsが必要となる。",
      "explanation": "MLOpsは、機械学習モデルのライフサイクル全体を管理し、品質を維持するための重要な考え方です。"
    }
  ]
}
"""

    user_prompt = f"""
以下の講義内容から、{num_questions}個のQAセットを難易度「{difficulty}」で作成してください。

---講義内容---
{lecture_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # 精度と速度のバランスが良いモデル
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {e}"