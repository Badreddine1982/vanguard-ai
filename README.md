# VANGUARD Pro - Self-Evolving Cognitive Agent

## ما هو VANGUARD؟

VANGUARD Pro هو وكيل ذكي (AI Agent) يقوم بتحليل المشاريع البرمجية وتشخيص الأخطاء
واقتراح الإصلاحات بشكل ذاتي التعلم، ويعرض كل ذلك عبر واجهة API.

## الميزات الرئيسية

- **تحليل AST**: استخراج ميزات حقيقية من الكود المصدري
- **شبكة عصبية**: اتخاذ قرارات ذكية بتعلم مستمر
- **ذاكرة متجهية**: تخزين واسترجاع الحلول السابقة (محلياً + Pinecone)
- **إصلاح ذاتي**: تطبيق الإصلاحات تلقائياً وإعادة المحاولة
- **واجهة API**: FastAPI
- **حاوية Docker**: نشر فوري على أي منصة

## البدء السريع

```bash
pip install -r requirements.txt
cp .env.example .env   # عدّل الملف حسب إعداداتك
python main.py
```

اختبار API:

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"project_path": "./"}'
```

## Docker

```bash
docker build -t vanguard-agent .
docker run -p 8000:8000 vanguard-agent
```

## نقاط API

| النقطة | الطريقة | الوصف |
|--------|---------|-------|
| `/analyze` | POST | تحليل مشروع برمجي |
| `/build` | POST | بناء المشروع مع تصحيح ذاتي |
| `/diagnose` | POST | تشخيص خطأ واقتراح حلول |
| `/feedback` | POST | تدريب الموجه العصبي على نتيجة صحيحة |
| `/stats` | GET | إحصائيات النظام |
| `/health` | GET | فحص صحة الوكيل |
| `/memory/{query}` | GET | البحث في الذاكرة |

## متغيرات البيئة

انظر `.env.example`. عند `VANGUARD_MOCK_LLM=true` يعمل النظام دون أي مفتاح LLM
ويعيد حلولاً احتياطية. الذاكرة تعمل محلياً افتراضياً، وتُستخدم Pinecone فقط عند
توفير `VANGUARD_PINECONE_API_KEY`.

## اختبار

```bash
pytest tests/ -v
```

## الترخيص

MIT License
