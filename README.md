# German Language Learning System

এই folder-টি তোমার German শেখার সম্পূর্ণ local workspace। Obsidian-এ `Dashboard.md` খুলে শুরু করবে।

## দ্রুত শুরু

1. [[Dashboard]] খুলে বর্তমান অবস্থা দেখো।
2. [[Syllabus]] থেকে learning journey দেখো।
3. নতুন practice শেষে `Lectures/`-এ তারিখসহ lecture note তৈরি করো।
4. Progress, ভুল এবং revision queue update করো।
5. পরের session-এর starting point fixed নয়; [[Agent]]-এর decision rules অনুসরণ করে নতুন agent তা নির্ধারণ করবে।
6. Chat ছাড়া নিজে revision দিতে [[Revision-Index]] খুলে lecture-এর practice ও answer key ব্যবহার করো।
7. Skill baseline দেখতে [[Baseline-Assessment]] খুলে দেখো।

## Obsidian ব্যবহার

- `[[নাম]]` ধরনের link-এ click করে related note খুলো।
- `Dashboard.md`-এর progress bar ও status table নিয়মিত update হবে।
- `Lectures/` হলো session-এর evidence archive।
- `Memory/` হলো compact long-term memory।
- প্রতিটি lecture-এ learner-facing revision sheet এবং agent-facing record দুটোই থাকে।

## মূল নিয়ম

Progress-এর কোনো দাবি evidence ছাড়া করা যাবে না। Unknown হলে সেটি `Unknown — needs assessment` হিসেবে লিখতে হবে।

## অন্য PC বা অন্য AI agent দিয়ে practice করার নিয়ম

এই project অন্য PC বা অন্য AI agent দিয়েও ব্যবহার করা যাবে। নতুন session শুরু করার সময় agent-কে নিচের instruction-টি দাও:

> এই project-এর `Agent.md` সম্পূর্ণ পড়ো। তারপর `Syllabus.md`, `Dashboard.md`, `Memory/Current-Progress.md`, `Memory/Error-Log.md`, `Memory/Revision-Queue.md`, `Memory/Revision-Index.md` এবং সর্বশেষ lecture file পড়ো। প্রয়োজন হলে সংশ্লিষ্ট cheatsheet ও vocabulary tracker পড়ো। এরপর আমার শেষ progress point থেকে ১০–১৫ মিনিটের German practice শুরু করো। আমাকে Bengali-তে grammar বুঝিয়ে German-এ practice করাও। প্রতিটি session শেষে YAML metadata-সহ learner revision sheet এবং agent record-সহ lecture file তৈরি করো; `Current-Progress.md`, `Error-Log.md`, `Revision-Queue.md`, `Session-Index.md` এবং সংশ্লিষ্ট vocabulary/grammar tracker evidence অনুযায়ী update করো। Starting point না থাকলে files-এর evidence দেখে নিজে নির্ধারণ করো। কোনো progress অনুমান করে লিখবে না।

### নতুন PC ব্যবহারের আগে

- সম্পূর্ণ `German Language Learning System` folder sync, copy অথবা Git-এর মাধ্যমে আনো।
- সর্বশেষ file version ব্যবহার করো।
- একই সময়ে দুই agent দিয়ে একই file edit করো না।
- অন্য agent কাজ শেষ করলে lecture, memory এবং tracker files save হয়েছে কি না যাচাই করো।
- Obsidian vault হিসেবে সম্পূর্ণ `German Language Learning System` folder open করো।

### Agent-এর পড়ার অগ্রাধিকার

1. `Agent.md`
2. `Memory/Current-Progress.md`
3. `Dashboard.md` এবং `Syllabus.md`
4. `Memory/Error-Log.md` ও `Memory/Revision-Queue.md`
5. সর্বশেষ lecture এবং সংশ্লিষ্ট cheatsheet/tracker

`Memory/Current-Progress.md` হলো canonical progress source; Dashboard শুধু summary।

## Open-source note

Before publishing this folder, review `External Resources/` for copyright and redistribution permissions. Keep only resources that you own, created, or are explicitly licensed to share.
