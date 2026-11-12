# 🇩🇪 Goethe B1 — vocabulary course

> **অবস্থা: আংশিক প্রস্তুত। পুরো Goethe list-এর coverage এখনও যাচাই শেষ হয়নি।**
>
> **প্রস্তুত:** ১০০টি target-এর ২০টি শেখার lesson + ৫টি revision lesson।
>
> **এটি ১০০টি শব্দ শেখা হয়ে গেছে—এমন দাবি নয়।** আগে জানা শব্দও এই course-এ আছে; সেগুলো ছোট recall check করে এগোবে।

## এখান থেকে শুরু

- [Lesson 1 — পরিচয় ও যোগাযোগ](<Lessons/GB1-L001.md>)
- [সমস্ত প্রস্তুত lesson](<Lesson-Index.md>)
- [A–Z lookup](<A-Z.md>) — candidate/unverified rows স্পষ্টভাবে চিহ্নিত।
- [কতটা source check হয়েছে, কী বাকি](<Coverage.md>)
- [প্রস্তুতির কাজের log](<Preparation-Log.md>)
- [Source ও publication boundary](<Source-Manifest.md>)

## শেখার পথ

পরিচয় → পরিবার → থাকা ও কথা বলা → কেনাকাটা → খাবার → বাসা → যাতায়াত → স্বাস্থ্য → সময় → প্রশ্ন/উত্তর → অল্প office vocabulary → দৈনন্দিন কাজ ও অনুভূতি।

সাধারণত প্রতি lesson-এ ৫টি target। প্রতি ৪টি নতুন-word lesson-এর পরে revision। এগুলো ২০ দিনেই শেষ করতে হবে এমন deadline নয়; recall অনুযায়ী একই lesson ছোট দুই session-এ করা যায়। আগে জানা শব্দ বেশি থাকলে short check করে দ্রুত এগোবে।

## একা পড়ার নিয়ম

1. শব্দের বাংলা অর্থ এবং উদাহরণ বোঝো। Noun-এর article/plural একসঙ্গে বলো।
2. Verb-এর pattern, Präsens, Partizip II, auxiliary ও case দেখো। সব verb-এর Präteritum এখনই মুখস্থ করতে হবে না; [[Prateritum-Priority-List]] অনুসরণ করো।
3. শব্দের অংশ ঢেকে practice করো; তারপর আলাদা Answer key দেখো।
4. যেগুলো ভুলে যাও শুধু সেগুলো বেশি revision দাও। প্রস্তাবিত interval: পরের session, প্রায় ৩ দিন, ১ সপ্তাহ, পরে আবার।
5. নিজের answer agent-কে দিলে dated lecture ও canonical trackers-এ exact evidence save হবে। নিজে checkbox tick করা self-check; তা দিয়ে agent score বা Stable status অনুমান করবে না।

## কোনো সংখ্যা কী বোঝায়

| সংখ্যা | অর্থ |
|---|---|
| ১০৪ page | downloaded source PDF-এর page count |
| প্রায় ২,৪০০ lexical unit | publisher-এর আনুমানিক বর্ণনা; exact imported count নয় |
| ২,৮৭৭ source block/page occurrence | automated extraction; word-group page-ও একটি unresolved block হতে পারে |
| ২,৭৩২ candidate target | provisional parsing/normalization; duplicates/merged entries/variants review বাকি |
| ১০০ checked teaching target | অর্থ/forms/example-সহ প্রস্তুত material; learner mastery নয় |
| ২০ + ৫ ready lesson | ২০টি new-word lesson ও ৫টি revision lesson |

বর্তমান machine-readable counts: `Data/Preparation-Counts.json`। Course preparation %, learner recall % ও B1 readiness এক জিনিস নয়। Full source review না হওয়া পর্যন্ত final target denominator অজানা।

## Agent continuation

- প্রথমে [[Agent]], [[Current-Progress]], latest dated lecture ও due revision পড়বে। এই course-এ প্রস্তুত material পাওয়া গেলেই learner-কে Introduced/Practiced ধরবে না।
- Practice চালাতে: আগে শেখা shopping/Termin/Vertrag-এর সংক্ষিপ্ত delayed check উপযোগী হলে করবে; তারপর প্রথম suitable ready lesson। Fixed next lesson না থাকলে evidence থেকে নিজে বেছে নেবে।
- Course বানানোর কাজ চালাতে: Preparation-Log → execution ledger → approved spec/plan পড়বে। বাকি candidate source reconciliation এবং lesson authoring চালিয়ে যাবে; প্রথম ১০০ target-কে পুরো source বলে ধরবে না।
- Prepared lessons এখানে; actual session records `Lectures/`-এ। Canonical vocabulary learning statuses কেবল পুরোনো word-type trackers-এ। Inventory-এর canonical links navigation/reference; live status-এর জন্য tracker পড়বে।

## Maintenance

Editable original teaching data: `Data/Authoring.json`। `Inventory.json`, Teaching/Lessons JSON ও A–Z/index notes generated views। Normalization-এর unresolved source entries হাতে review করে input data-তে ঠিক করতে হবে।

Individual content approval: `Data/Content-Approvals.json`। প্রতিটি reviewed word-এর meaning/forms/example/exercise/key revision-এর digest থাকে। নতুন বা বদলানো record স্বয়ংক্রিয় approval পায় না; আগের approval mismatch হলে lesson ready হয় না। Content পড়ে যাচাই না করে নতুন digest stamp করবে না। File-wide review label approval নয়। Withdrawn lesson-এর পুরোনো ready file withdrawal notice দিয়ে বদলায়; learner-edited file হলে overwrite না করে থামে, hash history রাখা হয়।

Vault root থেকে compatible Python দিয়ে:

```sh
python3 scripts/goethe_b1/build.py
python3 -m unittest discover -s scripts/goethe_b1/tests -v
python3 scripts/goethe_b1/validate.py Vocabulary/Wordlists/Goethe-B1 --vault .
python3 scripts/goethe_b1/validate.py Vocabulary/Wordlists/Goethe-B1 --vault . --require-complete
```

Extraction পুনরায় করতে pdfplumber-সহ Python দরকার; এই computer-এ bundled runtime ব্যবহার করা হয়েছে। অন্য PC-তে scripts চালানো বাধ্যতামূলক নয়—সব lesson ও index সাধারণ Markdown। Private PDF/cache Git-এ নেই; script rebuild-এর জন্য source আবার official URL থেকে আনতে হতে পারে।

Rebuild learner-edited lesson পেলে overwrite না করে থামবে; নিজের notes/checkmarks preserve করে তারপর reconcile করবে। `--require-complete` এখন **fail করাই প্রত্যাশিত**, কারণ সম্পূর্ণ coverage/lesson authoring বাকি। Normal partial-mode integrity pass কখনও complete-course pass নয়।

Validator lesson-এর metadata ও teaching/answer content reviewed data-এর সঙ্গে মিলিয়ে দেখে। Checkbox tick এবং নির্দিষ্ট Learner notes marker-এর মাঝের নিজের নোট content corruption নয়; তবে rebuild-এ নিজের edits preserve/reconcile করতে হবে।
