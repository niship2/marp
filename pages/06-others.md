---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
class: lead
---

## 6. その他資料

---

## 6-1. 全体まとめ

- 生成 AI をうまく活用するためのプロンプトエンジニアリング・コンテキストエンジニアリング
- プログラミングできなくても活用できる
- 自分の業務との掛け合わせ=**一般的な LLM だけではできない**領域

---

## 6-2. クイズ

---

## 問 1

個別の指示設計に焦点を当てる「プロンプトエンジニアリング」に対し、AI との対話全体を体系的に設計するアプローチを何と呼びますか？

A. コンテキストエンジニアリング
B. モデルチューニング
C. エージェント設計
D. RAG (検索拡張生成)

---

## 問 2

AI が自身の学習データにない最新情報や専門知識にアクセスし、回答の正確性を向上させるための技術（フレームワーク）は何ですか？

A. ファインチューニング
B. RAG (Retrieval Augmented Generation)
C. Chain of Thought (思考の連鎖)
D. マルチモーダル AI

---

## 問 3

AI エージェントを構成する 3 つの不可欠な要素として、資料で挙げられていないものはどれですか？

A. モデル (LLM)
B. ツール
C. オーケストレーション層
D. ユーザーインターフェース

---

## 問 4

従来の「あなたはプロの〇〇です」という役割を与えるプロンプトの限界を乗り越えるため、AI に「思考のレンズ」を設計するアプローチとして紹介されているものはどれですか？

A. Few-Shot Learning
B. ReAct フレームワーク
C. コグニティブ・デザイン（認知設計）
D. コンテキスト圧縮

---

## 問 5

資料で紹介されている、プログラミング不要で AI アプリケーションやワークフローを構築できる「ノーコードツール」の例として、不適切なものはどれですか？

A. Dify
B. n8n
C. FlowiseAI
D. Python

---

## 問 6

Microsoft が提唱中で、プロンプトの設計と管理を体系化するためのマークアップ言語は何ですか？

A. XML
B. HTML
C. POML (Prompt Orchestration Markup Language)
D. LCEL (LangChain Expression Language)

---

## 問 7

自作で RAG・AI Agent を開発する場合と、クラウドサービスを利用する場合の比較において、一般的に自作開発が優れている点はどれですか？

A. 開発時間
B. 運用負荷
C. カスタマイズ性
D. 最新技術へのアクセス

---

## 問 8

AI にタスクを依頼する際、「ステップバイステップで考えてください」と一言加えるだけで、複雑な問題に対する回答の精度を向上させる効果が期待できるプロンプト技術は何ですか？

A. Few-Shot Learning
B. Zero-shot Chain-of-Thought
C. ReAct
D. Role Playing

---

## 問 9

複数の AI エージェントにそれぞれ専門的な役割を割り当て、分業と協調作業によって複雑なタスクを遂行する AI エージェントのデザインパターンは何ですか？

A. Debate-based Cooperation（討論ベースの協調）
B. Cross-Reflection（相互省察）
C. Role-based Cooperation（役割ベースの協調）
D. Human Reflection（人間による省察）

---

## 問 10

コマンドライン（ターミナル）から直接 AI を利用し、スクリプト化やファイル操作の自動化を容易にするツールとして紹介されているものはどれですか？

A. LangChain
B. Cursor
C. Dify
D. GeminiCli / Claude Code CLI

---

## 解答

1.  **A. コンテキストエンジニアリング**
2.  **B. RAG (Retrieval Augmented Generation)**
3.  **D. ユーザーインターフェース**
4.  **C. コグニティブ・デザイン（認知設計）**
5.  **D. Python**
6.  **C. POML (Prompt Orchestration Markup Language)**
7.  **C. カスタマイズ性**
8.  **B. Zero-shot Chain-of-Thought**
9.  **C. Role-based Cooperation（役割ベースの協調）**
10. **D. GeminiCli / Claude Code CLI**

---

## 6-3. 参考文献

---

### 論文・学術情報 (arXiv)

[1] ReAct: Synergizing Reasoning and Acting in Language Models  
https://arxiv.org/abs/2210.03629

[2] The Prompt Report: A Systematic Survey of Prompt Engineering Techniques  
https://arxiv.org/abs/2406.06608

[3] Agent Design Pattern (論文)  
https://arxiv.org/html/2405.10467v4

[4] Constitutional AI: Harmlessness from AI Feedback  
https://arxiv.org/abs/2212.08073

[5] Structure Guided Prompt: Instructing Large Language Model in Multi-Step Reasoning by Exploring Graph Structure of the Text  
https://arxiv.org/abs/2402.13415

---

[6] When "A Helpful Assistant" Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models  
https://arxiv.org/abs/2311.10054

---

### 技術解説・ブログ記事

[7] 生成 AI の AI エージェントを大手 3 社（AWS、Azure、Google Cloud）で徹底比較してみた  
https://blog.g-gen.co.jp/entry/comparing-agent-architecture-across-cloud-vendors

[8] 生成 AI の RAG 構成を大手 3 社で徹底比較  
https://blog.g-gen.co.jp/entry/comparing-rag-architecture-across-cloud-vendors

[9] 生成 AI のよくある誤解を整理して AI の業務活用を推進する  
https://blog.g-gen.co.jp/entry/clearing-up-misconceptions-about-generative-ai

[10] 【プロンプト技術 58 種類の 9 割は「無駄」だった...】実例 2,000 件から学ぶ！LLM 時代の"強いプロンプトテンプレート"設計術 (GMO インターネットグループ)  
https://recruit.gmo.jp/engineer/jisedai/blog/prompt_template/

[11] 「あなたはプロの〇〇です」をもうやめたい (Qiita)  
https://qiita.com/makotosaekit/items/0eccb562bf7d3f66fbfa

---

[12] Context Engineering for Agents (LangChain Blog)  
https://blog.langchain.com/context-engineering-for-agents/

[13] Context Engineering Guide (Prompting Guide)  
https://www.promptingguide.ai/guides/context-engineering-guide

[14] Context Engineering with LLMs (Phil Schmid's Blog)  
https://www.philschmid.de/context-engineering

[15] LLM へのプロンプトを構造化された文書で管理する POML (azukiazusa.dev)  
https://azukiazusa.dev/blog/poml-prompt-structured-document/

[16] AWS Bedrock の Knowledge base で RAG アプリを実装してみた (NRI ネットコム)  
https://tech.nri-net.com/entry/aws_bedrock_rag_app

---

[17] Azure OpenAI Service の「On Your Data」とは？ (NTT 東日本)  
https://business.ntt-east.co.jp/content/cloudsolution/column-628.html

[18] MCP(Model Context Protocol)の紹介 (CloudNative Inc. Blog)  
https://blog.cloudnative.co.jp/27994/

[19] Agent Communication Protocol について (Qiita)  
https://qiita.com/okikusan-public/items/196f1a781b3bf33536aa

[20] Agent Design Pattern の解説 (Qiita)  
https://qiita.com/Chi_corp_123/items/cf26215878cad285599b

---

### 各種ガイド・資料

[21] Vellum AI LLM Leaderboard  
https://www.vellum.ai/llm-leaderboard

[22] 特許用プロンプト例 (Google Sheets)  
https://docs.google.com/spreadsheets/d/1bh1X3BGT8x99OSos19TrRpOUQGN9kqhyKK2v-r3tcWI/edit?usp=sharing

[23] GPT-5 prompting guide (OpenAI Cookbook)  
https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide

[24] Claude 4 プロンプトエンジニアリングのベストプラクティス (Anthropic)  
https://docs.anthropic.com/ja/docs/build-with-claude/prompt-engineering/claude-4-best-practices

[25] Google prompting guide 101 (Google)  
https://services.google.com/fh/files/misc/gemini-for-google-workspace-prompting-guide-101.pdf

---

[26] RAG From Scratch (GitHub)  
https://github.com/langchain-ai/rag-from-scratch

[27] Google Cloud Architecture Center - Generative AI for RAG  
https://cloud.google.com/architecture/ai-ml/generative-ai-rag?hl=ja

[28] Google Codelabs - Building AI Agents with Vertex AI  
https://codelabs.developers.google.com/devsite/codelabs/building-ai-agents-vertexai?hl=ja#2

[29] patentsearchagent (GitHub)  
https://github.com/niship2/patentsearchagent

[30] POML (Prompt Orchestration Markup Language) (GitHub)  
https://github.com/microsoft/poml

---

[31] Playwright MCP を使って特許調査  
https://www.enlighton.co.jp/post/playwright-mcp%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E7%89%B9%E8%A8%B1%E8%AA%BF%E6%9F%BB

[32] FlowHunt USPTO Patent MCP  
https://www.flowhunt.io/integrations/uspto/

[33] Google Patents MCP Server  
https://github.com/KunihiroS/google-patents-mcp

[34] プロンプトジェネレータツール比較  
https://miralab.co.jp/media/prompt_generator_recommendations/

[35] 知財バージョン/私作成  
https://ip-prompt-generator-for-llms-222593271342.us-west1.run.app/

---

[36] プロンプト研究の論文紹介  
https://note.com/rami_engineer/n/n8ecd7ac00cc4

[37] Baby AGI: Task-driven Autonomous Agent  
https://yoheinakajima.com/task-driven-autonomous-agent-utilizing-gpt-4-pinecone-and-langchain-for-diverse-applications/

[38] 現場で活用するための AI エージェント実践入門  
https://www.kspub.co.jp/book/detail/5401408.html

[39] Deep Agents (LangChain Blog)  
https://blog.langchain.com/deep-agents/

[40] Deep Agents with LangGraph (無料コース)  
https://academy.langchain.com/courses/deep-agents-with-langgraph

---

[41] Deep Agents from Scratch (GitHub)  
https://github.com/langchain-ai/deep-agents-from-scratch/blob/main/notebooks/4_full_agent.ipynb

[42] X 投稿: RAG システムの工夫点  
https://x.com/athleticKoder/status/1968658987756224919

[43] GitHub: marp  
https://github.com/niship2/marp

[44] ChatGPT  
https://chat.openai.com

[45] Claude  
https://claude.ai

---

[46] Gemini  
https://gemini.google.com

[47] Google AI Studio  
https://aistudio.google.com/

[48] AI0W - AI Agents  
https://ai0w.com/agents/

[49] Dify  
https://dify.ai/

[50] n8n  
https://n8n.io/

---

[51] FlowiseAI  
https://flowiseai.com/

[52] LangFlow  
https://www.langflow.org/

[53]Effective context engineering for AI agents
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

---

### 2026 年以降のトレンド関連参考資料

[54] EU AI Act (EUR-Lex 公式テキスト)
https://eur-lex.europa.eu/eli/reg/2024/1689/oj

[55] USPTO Inventorship Guidance for AI-Assisted Inventions
https://www.uspto.gov/initiatives/artificial-intelligence

[56] 文化庁 AI と著作権に関する考え方について
https://www.bunka.go.jp/seisaku/chosakuken/aiandcopyright.html

[57] 内閣府 AI 戦略・AI 推進法関連資料
https://www8.cao.go.jp/cstp/ai/

---

[58] Anthropic Computer Use (developer docs)
https://docs.anthropic.com/en/docs/build-with-claude/computer-use

[59] OpenAI Operator / Computer-using agents
https://openai.com/index/introducing-operator/

[60] DABUS 判例の各国比較（WIPO Magazine 等）
https://www.wipo.int/wipo_magazine/en/

[61] Sovereign AI / オープンウェイトモデル動向 (Hugging Face)
https://huggingface.co/blog

[62] Defensive Publication と AI 生成先行技術に関する議論 (IP Watchdog 等)
https://ipwatchdog.com/

---

### ハーネスエンジニアリング関連参考資料

[63] Martin Fowler "Harness engineering for coding agent users"
https://martinfowler.com/articles/harness-engineering.html

[64] Mitchell Hashimoto / Martin Fowler "Harness Engineering - first thoughts"
https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html

[65] OpenAI "Harness engineering: leveraging Codex in an agent-first world"
https://openai.com/index/harness-engineering/

[66] LangChain "The Anatomy of an Agent Harness"
https://www.langchain.com/blog/the-anatomy-of-an-agent-harness

[67] awesome-harness-engineering (GitHub)
https://github.com/ai-boost/awesome-harness-engineering

---

[68] AddyOsmani.com "Agent Harness Engineering"
https://addyosmani.com/blog/agent-harness-engineering/

[69] HumanLayer "Skill Issue: Harness Engineering for Coding Agents"
https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents

[70] Firecrawl "What Is an Agent Harness?"
https://www.firecrawl.dev/blog/what-is-an-agent-harness

[71] Parallel "What is an agent harness in the context of LLMs?"
https://parallel.ai/articles/what-is-an-agent-harness

[72] MongoDB "The Agent Harness: Why the LLM Is the Smallest Part of Your Agent System"
https://www.mongodb.com/company/blog/technical/agent-harness-why-llm-is-smallest-part-of-your-agent-system

---

### 2026 年 知財 × 生成 AI ニュース関連参考資料

[73] USPTO Revised Inventorship Guidance for AI-Assisted Inventions (2025-11-28)
https://www.federalregister.gov/documents/2025/11/28/2025-21457/revised-inventorship-guidance-for-ai-assisted-inventions

[74] Holland & Knight "The Final Word? Supreme Court Refuses to Hear Case on AI Authorship and Inventorship"
https://www.hklaw.com/en/insights/publications/2026/03/the-final-word-supreme-court-refuses-to-hear-case-on-ai-authorship

[75] Venable "The §101 Reset for 2026: New USPTO Guidance on AI Eligibility"
https://www.venable.com/insights/publications/2025/12/the-101-reset-for-2026

[76] Bartz v. Anthropic 和解報道 (ITmedia)
https://www.itmedia.co.jp/news/articles/2509/06/news037.html

[77] Anthropic 著作権侵害和解（時事ドットコム）
https://www.jiji.com/jc/article?k=2025090600264&g=int

---

[78] AI Business "AI Lawsuits in 2026: Settlements, Licensing Deals, Litigation"
https://aibusiness.com/generative-ai/ai-lawsuits-in-2026-settlements-licensing-deals-litigation

[79] Norton Rose Fulbright "An update on AI copyright cases in 2026"
https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026

[80] Latham & Watkins "EU AI Act: GPAI Model Obligations in Force and Final GPAI Code of Practice in Place"
https://www.lw.com/en/insights/eu-ai-act-gpai-model-obligations-in-force-and-final-gpai-code-of-practice-in-place

[81] Kennedys "EU AI Act implementation timeline (2026 deadline)"
https://www.kennedyslaw.com/en/thought-leadership/article/2026/the-eu-ai-act-implementation-timeline-understanding-the-next-deadline-for-compliance/

[82] GVA法律事務所「2026 年最新 AI 事業者ガイドライン改訂の要点」
https://gvalaw.jp/blog/i20260303/

---

[83] 日経新聞「生成 AI 用いた知財侵害を抑制 特許庁、企業の開発保護」
https://www.nikkei.com/article/DGXZQOUA050P20V01C24A1000000/

[84] 共同通信 / Yahoo!ニュース「生成 AI の『知財』侵害を防ぐ 特許庁、26 年に意匠法改正へ」
https://news.yahoo.co.jp/articles/549fd68cfec75584834175f7f9dcbce5bc6af84e

[85] JPO「AI 関連発明の出願状況調査」
https://www.jpo.go.jp/system/patent/gaiyo/sesaku/ai/ai_shutsugan_chosa.html

[86] JPO「AI 関連技術に関する特許審査の事例について」
https://www.jpo.go.jp/system/laws/rule/guideline/patent/ai_jirei.html

[87] Business Insider「NEC が知財 AI 開発で実現した『最大 94% 効率化』」
https://www.businessinsider.jp/article/2601-nec-ai-intellectual-property-efficiency/

---

[88] Intelacia "Harvey's $11B Valuation"
https://www.intelacia.com/2026/05/05/harveys-11b-valuation-how-legal-ai-is-reshaping-modern-legal-workflows/

[89] LexisNexis × Harvey 戦略提携
https://www.lexisnexis.com/community/pressroom/b/news/posts/lexisnexis-and-harvey-announce-strategic-alliance-to-integrate-trusted-high-quality-ai-technology-and-legal-content-and-develop-advanced-workflows

[90] PatSnap "Top 6 IP Patent Search Platforms for 2026"
https://www.patsnap.com/resources/blog/articles/top-6-ip-patent-search-platforms-for-2026/

[91] Research and Markets / SNS Insider "AI Patent Search Market Report 2026"
https://www.researchandmarkets.com/reports/6226574/ai-patent-search-market-report

[92] 文化庁「AI と著作権について」
https://www.bunka.go.jp/seisaku/chosakuken/aiandcopyright.html

---

### Evals・運用・セキュリティ関連参考資料

[93] OpenAI Evals (GitHub)
https://github.com/openai/evals

[94] Langfuse (LLM 観測 + 評価 OSS)
https://langfuse.com/

[95] LangSmith Evaluation
https://docs.smith.langchain.com/evaluation

[96] Arize Phoenix (OSS 観測・評価)
https://phoenix.arize.com/

[97] Braintrust
https://www.braintrust.dev/

[98] DeepEval (pytest 互換 LLM 評価)
https://github.com/confident-ai/deepeval

[99] NIST AI Risk Management Framework
https://www.nist.gov/itl/ai-risk-management-framework

---

[100] OWASP Top 10 for LLM Applications
https://owasp.org/www-project-top-10-for-large-language-model-applications/

[101] Helicone (LLM コスト・観測)
https://www.helicone.ai/

[102] Microsoft Prompt flow (Evals 統合)
https://github.com/microsoft/promptflow

---

### 2026 年 主要モデル・ツールアップデート 参考資料

[103] Anthropic Release Notes
https://platform.claude.com/docs/en/release-notes/overview

[104] OpenAI Release Notes
https://help.openai.com/en/articles/12591856-chatgpt-atlas-release-notes

[105] Gemini Apps Release Notes
https://gemini.google/release-notes/

[106] Anthropic "Introducing Claude Opus 4.7"
https://www.anthropic.com/news/claude-opus-4-7

[107] Vellum "Claude Opus 4.7 Benchmarks Explained"
https://www.vellum.ai/blog/claude-opus-4-7-benchmarks-explained

---

[108] OpenAI "Introducing GPT-5.5"
https://openai.com/index/introducing-gpt-5-5/

[109] OpenAI "Introducing ChatGPT Atlas"
https://openai.com/index/introducing-chatgpt-atlas/

[110] OpenAI "Introducing ChatGPT Agent: bridging research and action"
https://openai.com/index/introducing-chatgpt-agent/

[111] Google "Gemini 3.1 Pro: A smarter model for your most complex tasks"
https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/

[112] Google "Introducing Gemini 3 Flash"
https://blog.google/products/gemini/gemini-3-flash/

---

[113] Google Cloud "Gemini 3.1 Flash-Lite is now generally available"
https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-1-flash-lite-is-now-generally-available

[114] Google DeepMind "Project Mariner"
https://deepmind.google/models/project-mariner/

[115] The Next Web "Google Cloud Next 2026: AI agents, A2A, Workspace Studio"
https://thenextweb.com/news/google-cloud-next-ai-agents-agentic-era

[116] Anthropic "Claude Computer Use Agent"
https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool

[117] Anthropic Agent Skills (Docs)
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

[118] Simon Willison "Live blog: Code w/ Claude 2026"
https://simonwillison.net/2026/May/6/code-w-claude-2026/

[119] VentureBeat "OpenAI unveils Workspace Agents"
https://venturebeat.com/orchestration/openai-unveils-workspace-agents-a-successor-to-custom-gpts-for-enterprises-that-can-plug-directly-into-slack-salesforce-and-more

---

### 日本企業の知財 × AI / 生成 AI サービス 参考資料

[120] 島津製作所「Genzo AI 設立リリース」
https://www.shimadzu.co.jp/news/2026/acmnk57uqb3579ay.html

[121] Genzo AI 公式
https://www.genzo-ai.co.jp/

[122] Tokkyo.Ai 公式（リーガルテック株式会社）
https://www.tokkyo.ai/

[123] AI Samurai 公式
https://aisamurai.co.jp/

[124] Patentfield 公式
https://en.patentfield.com/

[125] サマライア（Summaria）
https://patent-i.com/summaria/

---

[126] ユアサポAI 公式
https://yoursup.co.jp/

[127] アッピアエンジン（appia-engine） / Smart-IP
https://yorozuipsc.com/uploads/1/3/2/5/132566344/19bc4f1da0c0e2e3d76c.pdf

[128] Toreru Media「生成 AI は知財業務にどんな影響を与えるのか？」
https://toreru.jp/media/trademark/7924/

[129] IP Force 知財ポータル
https://ipforce.jp/

[130] Biz/Zine「京セラ・島津製作所・旭化成の知財責任者が語る AI エージェント時代」
https://bizzine.jp/article/detail/11579?p=2

[131] 日経新聞「島津製作所、知財業務を AI で効率化 新会社でサービス外販」
https://www.nikkei.com/article/DGXZQOUF251520V20C26A3000000/

[132] MONOist「年間 8000 万円のコストを削減した知財業務自動化 AI を外販」
https://monoist.itmedia.co.jp/mn/articles/2604/02/news040.html

---

[133] パナソニック × 富士通 × 三菱電機 AI 検索共同開発
https://pr.fujitsu.com/jp/news/2019/11/1.html

[134] AI 特許文書作成支援サービス比較レポート (yorozuipsc)
https://yorozuipsc.com/uploads/1/3/2/5/132566344/6d203dddf3e173d61aa8.pdf
