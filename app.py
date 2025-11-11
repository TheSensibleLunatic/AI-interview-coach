import os
import whisper
import json
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime


# --- 1. CONFIGURE YOUR API KEY ---
GEMINI_API_KEY = "AIzaSyAdDE1g68f55NaRBbZWcKOiwzVCPyZocKE"
# --- End Configuration ---


# --- 2. CAMPUS PLACEMENT INTERVIEW QUESTIONS FOR FINAL YEAR STUDENTS ---
INTERVIEW_QUESTIONS = [
    {
        "question": "You're in the final round of interviews at a dream product-based company (Google/Microsoft level). Your college placement cell just informed you that TCS is also offering you a role with immediate joining, and they need your decision in 2 hours. Your parents want job security. What do you do?",
        "expected_answer": "During my final year placement season, I faced exactly this dilemma between a stable service company offer and waiting for a dream product company result (Situation). I needed to make a decision that balanced family expectations, career growth, and ethical commitments to both companies (Task). First, I called the TCS HR and politely explained my situation, requesting a 24-hour extension which they granted. Then I immediately contacted the product company's recruiter, explained I had a deadline, and asked for an expedited decision. I also had an honest conversation with my parents, showing them salary projections and growth trajectories - product companies offer 40% faster career growth and 2x salary hikes. I prepared a backup plan: if the product company rejected me, TCS was still a respected start (Action). The product company appreciated my transparency and fast-tracked my result - I got the offer with ₹18 LPA vs TCS's ₹3.5 LPA. I professionally declined TCS, thanking them genuinely. My parents were convinced by the data, and I joined the product company where I learned advanced system design and got promoted within 18 months. The key lesson: always communicate transparently and never burn bridges - that TCS recruiter later helped me hire for my team (Result).",
        "key_points": [
            "Request extension from first company professionally",
            "Communicate honestly with competing company about deadline",
            "Use data to convince parents (salary trajectory, growth, learning)",
            "Prepare backup plan while pursuing dream option",
            "Maintain professional relationships with all parties",
            "Quantify outcomes (18 LPA vs 3.5 LPA, 40% faster growth, 18-month promotion)"
        ]
    },
    {
        "question": "During your 6-month internship at a startup in Bangalore, you built a critical feature solo. Now in final year placement season, your team lead asks you to stay back full-time. However, you've also cleared 3 rounds at Amazon with final round pending. Your college has a strict 'no backing out' policy once you accept. What's your decision?",
        "expected_answer": "In my pre-final year summer internship at a Bangalore-based fintech startup, I built their entire payment reconciliation system that processed ₹50 lakh daily transactions (Situation). The team lead offered me a full-time role at ₹12 LPA with 0.5% equity, but I was also interviewing with Amazon for an SDE-1 role at ₹28 LPA. My college's placement policy stated that accepting any offer blocks you from further interviews (Task). I analyzed both options thoroughly: the startup offered faster learning, more ownership, and potential equity upside but higher risk and lower initial pay. Amazon offered brand value, better work-life balance, structured learning, and significantly higher compensation with job security. I created a decision matrix with 5-year projections. I then spoke to 3 alumni - one who joined a startup (now a VP), one at Amazon (now SDE-3), and one who switched from startup to FAANG after 2 years. Based on their inputs, I decided to pursue Amazon because as a fresher, I needed strong foundational training, financial stability for my family, and the flexibility to join startups later with better leverage (Action). I respectfully declined the startup offer, clearly explaining my reasoning. They understood and agreed to stay in touch. I cleared Amazon's final round and joined at ₹28 LPA. After 3 years at Amazon with strong fundamentals, I'm now evaluating founding my own startup with much better preparation. The startup I interned at got acquired, and I maintained great relations with the team - they're now my advisors (Result).",
        "key_points": [
            "Analyze both options with concrete data (salary, learning, risk, equity)",
            "Create decision matrix for systematic evaluation",
            "Consult multiple alumni with different paths",
            "Consider family financial situation and career stage",
            "Professional communication while declining",
            "Quantify everything (₹50L transactions, 12 LPA vs 28 LPA, 5-year projection, 3 years experience)"
        ]
    },
    {
        "question": "You're leading your final year project team of 4 students. Two weeks before the project demonstration to external examiners and placement panel, you discover one teammate copied 60% of the code from GitHub without attribution. This could disqualify your entire team and affect placement eligibility. What do you do?",
        "expected_answer": "During the final semester of my B.Tech at a Tier-2 college in Pune, our team was building an AI-based crop disease detection system for farmers (Situation). With just 14 days left before demonstration to external examiners who would grade us and the placement committee who would evaluate our project, I discovered through a code similarity checker that our backend developer, Rohan, had copied 1200 out of 2000 lines from a GitHub repository without any attribution or license compliance. This violated both our college's academic integrity policy and open-source license terms. If discovered during examination, our entire team of 4 would face disqualification, potentially losing placement eligibility, and I as team lead would bear primary responsibility (Task). First, I documented everything with screenshots, timestamps, and license violations. Then I called an emergency team meeting and presented the evidence without anger. Rohan initially got defensive but admitted he panicked due to poor time management and his mother's hospitalization. I empathized but explained the severe consequences. We had three options: (1) Restart from scratch - impossible in 14 days, (2) Report to faculty - would lead to disqualification, or (3) Rewrite properly with attribution in remaining time. I divided the 1200 lines among all 4 members - 300 lines each. I personally took 400 lines and we worked 16-hour days. I implemented proper git commits with 'Refactored' messages, added comprehensive README with attributions to original repos, and ensured all licenses were respected (Action). We completed with 2 days to spare and got 92/100 in evaluation - examiners specifically praised our code quality and proper attribution practices. All four team members got placed: I joined Flipkart at ₹14 LPA, two others joined Infosys and Wipro at ₹3.5 LPA each, and Rohan cleared Capgemini at ₹4 LPA. More importantly, Rohan learned a crucial lesson about integrity - he later thanked me and we're still friends. I learned crisis management, team leadership under pressure, and the importance of code reviews throughout the project, not just at the end. Our project was showcased in the college magazine, and I was awarded 'Best Project Lead' by the placement cell (Result).",
        "key_points": [
            "Document evidence thoroughly before confrontation",
            "Handle situation privately with empathy but clarity on consequences",
            "Present multiple solution options with trade-offs",
            "Take personal responsibility and lead by example (400 lines personally)",
            "Transform crisis into learning moment for entire team",
            "Quantify outcomes (1200/2000 lines, 92/100 grade, all 4 placed, salary ranges, 16-hour days, 14-day deadline)"
        ]
    },
    {
        "question": "In your placement aptitude test at Infosys, you notice the student next to you is using a smartwatch to cheat. The invigilator hasn't noticed. If you report it, you might be seen as a snitch by peers. If you don't, it's unfair to honest students. What do you do?",
        "expected_answer": "During Infosys campus placement drive at my college in Hyderabad in August of final year, we had 450 students appearing for the aptitude test with only top 50 proceeding to technical rounds (Situation). Halfway through the 60-minute test, I noticed Aditya, sitting to my right, constantly glancing at his smartwatch and typing answers. The 3 invigilators were monitoring the large hall but hadn't noticed. I faced a moral dilemma: reporting might make me unpopular among peers who value 'bro code,' but staying silent meant an unethical person might take a deserving candidate's slot. If Aditya cleared and I didn't, I would regret my silence. More fundamentally, this violated the integrity I wanted to build my career on (Task). I chose to act immediately but smartly. First, I raised my hand and called an invigilator over. When she came, I whispered 'I think the person next to me might be using their smartwatch for answers - I'm not certain but wanted to inform you.' I phrased it as uncertainty to avoid direct confrontation. The invigilator observed Aditya for 2 minutes and caught him red-handed checking his watch. She confiscated it, issued a warning, and he was disqualified from the drive. I focused back on my test (Action). I scored 82/100 and ranked 12th, clearing the cutoff of 75/100. I proceeded through technical rounds and received an offer at ₹3.6 LPA. Aditya was angry initially, but 6 months later during final semester, he approached me and apologized, saying the disqualification was a wake-up call - he focused on genuine preparation, cleared TCS later at ₹3.3 LPA, and realized shortcuts don't build careers. Some peers criticized me initially, but most respected my integrity. During my Infosys interview, the panel already knew about the incident (the invigilator had informed them) and they specifically appreciated my ethics - it became a positive talking point. Three years into my career, I'm known in my team for integrity and have been trusted with sensitive client data worth $2M. The key lesson: short-term popularity doesn't matter - long-term integrity defines your career. I'd make the same choice again (Result).",
        "key_points": [
            "Act immediately when witnessing unethical behavior",
            "Report professionally and factually without being accusatory",
            "Focus on fairness to all deserving candidates",
            "Don't compromise personal integrity for peer approval",
            "Long-term career reputation matters more than short-term popularity",
            "Quantify context (450 students, top 50 qualify, 82/100 score, rank 12, ₹3.6 LPA offer, $2M client trust, 3 years career impact)"
        ]
    },
    {
        "question": "You cleared all rounds at Zomato for an SDE role at ₹16 LPA. Your college placement rules state you must attend 3 more company drives before accepting. However, Zomato needs your acceptance within 48 hours or they'll offer it to someone else. What do you tell the placement cell and Zomato?",
        "expected_answer": "In November of my final year at VIT Vellore, I cleared 4 rounds of interviews at Zomato - aptitude, 2 technical rounds with system design, and HR - for an SDE-1 position at ₹16 LPA CTC (₹12.8 LPA fixed + ₹3.2 LPA variable) (Situation). This was my first offer and significantly above the college average of ₹6.5 LPA. However, our placement cell had a policy requiring students to participate in at least 3 more company drives before accepting any offer, to ensure maximum opportunities. The drives coming up were: Accenture (₹4.5 LPA), Cognizant (₹4.2 LPA), and L&T Infotech (₹5 LPA). Simultaneously, Zomato's HR called saying they needed my confirmation within 48 hours as they had 2 offers out and only 1 position remaining for our campus. I was caught between official college policy and a deadline from a company offering 2.5x the average package (Task). I immediately took two parallel actions. First, I scheduled an urgent meeting with our placement coordinator, Professor Ramesh, and the Training & Placement Officer. I presented the situation transparently with data: I showed them Zomato's offer letter with the 48-hour deadline clause, explained that Zomato was a Series D funded startup with excellent learning opportunities in high-scale systems (200M+ orders), and emphasized that the ₹16 LPA package would significantly contribute to the college's average placement statistics which impacts our ranking. I requested a one-time exception citing these factors. Simultaneously, I emailed Zomato HR explaining that I was extremely interested (I'd researched their tech stack and sent a detailed 'Why Zomato' document I'd prepared) but needed 72 hours instead of 48 to complete college formalities. I positioned this as formal paperwork, not negotiation (Action). The placement cell agreed to grant an exception after verifying Zomato's credibility and seeing my genuine preparation (my 'Why Zomato' doc impressed them). They made me sign an undertaking that I'd accept and wouldn't interview further. Zomato granted the 24-hour extension. I accepted the offer within 72 hours, completing all documentation. I joined Zomato post-graduation and worked on their delivery optimization system that reduced average delivery time by 12% across 3 cities. The ₹16 LPA offer also positively impacted my college's placement report, and Professor Ramesh used my case as an example for future batches on how to handle such situations professionally. Two years later, I referred 4 students from VIT to Zomato, giving back to both institutions. The key lessons: always communicate transparently with data, present win-win solutions, and show genuine preparation to demonstrate you're serious about the opportunity (Result).",
        "key_points": [
            "Present situation to both parties with complete transparency and data",
            "Show how your decision benefits all stakeholders (college ranking, company hire quality)",
            "Demonstrate genuine preparation and interest (research document)",
            "Request exception with valid business reasoning, not emotions",
            "Negotiate professionally with specific asks (72 hours vs 48 hours)",
            "Quantify everything (₹16 LPA vs ₹6.5 avg, 200M+ orders, 12% delivery optimization, 2.5x average package, 4 referrals, 3 cities impact)"
        ]
    },
    {
        "question": "During your Accenture group discussion for campus placement, one dominating candidate is speaking for 90% of the time and not letting others speak. The evaluator is noting everything. You have barely spoken. How do you handle this situation?",
        "expected_answer": "In September of my final year, Accenture visited my college NITK Surathkal for campus recruitment. After clearing the aptitude test, 60 of us were divided into groups of 8 for group discussions (Situation). My group's topic was 'AI replacing jobs vs creating jobs.' One candidate, Prateek from CSE with a 9.2 CGPA, started speaking immediately and dominated the conversation. By the 8-minute mark of the 15-minute GD, he had spoken for approximately 7 minutes continuously, not giving others space. Three quieter students, including me, had barely contributed. The evaluator, Ms. Sharma, was taking extensive notes and observing everyone's body language. I had strong points about AI in healthcare and agriculture creating new job categories, but couldn't find an opening. I needed to contribute meaningfully without appearing aggressive or making Prateek look bad, as evaluators assess both content and collaboration skills (Task). I used a strategic three-step approach. First, I actively listened and noted down 2-3 valid points Prateek made. At minute 9, when Prateek paused briefly to drink water, I made eye contact with the evaluator and said, 'I'd like to build on Prateek's excellent point about AI automation in manufacturing. While that's true, there's an important counter-example: According to a 2024 NASSCOM report, AI has created 4.2 lakh new jobs in India in roles like prompt engineering, AI ethics consulting, and data annotation that didn't exist 5 years ago.' This approach acknowledged his point (showing collaboration) while adding new data-driven content (showing value). Second, I actively facilitated others by turning to the quiet student next to me, Shruti, and saying, 'Shruti, you mentioned in our project review last week about AI in education - would you like to share that perspective here?' This demonstrated leadership and inclusivity. Third, when Prateek tried to interrupt Shruti, I politely but firmly gestured 'one moment' and said 'Let's hear her complete thought, then you can add' - this showed assertiveness in maintaining fairness (Action). In the final 6 minutes, the discussion became more balanced. I contributed 3 more substantial points with data (₹12,000 crore investment in Indian AI startups in 2024, AI-driven precision agriculture increasing farmer incomes by 30%, and specific examples of AI job creation in tier-2 cities). I ensured I spoke clearly, made eye contact with all group members, and twice explicitly involved others: 'Rahul, from your mechanical background, how do you see AI impacting core engineering roles?' Out of 8 members in my group, 4 cleared to the next round - Prateek was NOT one of them despite his subject knowledge and confidence. I was selected, along with Shruti and two others who contributed quality points. The evaluator specifically mentioned in her feedback during my personal interview that I 'demonstrated excellent leadership by balancing assertiveness with collaboration, bringing in data-driven points, and ensuring equal participation - these are traits we look for in Accenture consultants.' I ultimately received an offer at ₹4.5 LPA. The key lessons: In GDs, quality beats quantity always; evaluators watch how you enable others, not just your own points; use data and examples instead of generic statements; and strategic pauses and facilitation demonstrate more leadership than continuous speaking (Result).",
        "key_points": [
            "Listen actively and build on others' points, showing collaboration",
            "Time your entry strategically (natural pause, eye contact with evaluator)",
            "Use data-driven content (NASSCOM report, ₹12,000 cr investment, 30% farmer income increase, 4.2 lakh jobs)",
            "Actively facilitate quieter members to demonstrate inclusive leadership",
            "Balance assertiveness with respect when managing dominant speakers",
            "Quantify everything (8-member group, 15-min duration, 4 selected out of 8, ₹4.5 LPA offer, specific statistics)"
        ]
    },
    {
        "question": "You're interning at your dream company (Flipkart/Swiggy level) where return offers are given to top performers. Your manager assigns you a critical bug fix. You realize the entire architecture approach is flawed and needs 2 weeks to fix properly, but your manager wants a quick patch in 2 days. Your internship evaluation is in 3 weeks. What do you do?",
        "expected_answer": "During my pre-placement internship in January of final year at Swiggy's Bangalore office, I was part of the restaurant partner onboarding team as a backend intern (Situation). In my 5th week, our production system started showing 15% failed onboarding API calls. My manager, a Senior SDE with 6 years experience, assigned me to fix it urgently as restaurants were complaining they couldn't register, directly impacting business revenue - each day of downtime cost approximately ₹8 lakh in lost new partnerships. He needed a fix in 2 days for a deployment before the weekend. I dug into the codebase and discovered the real issue: the previous intern had used synchronous database calls with no connection pooling, causing timeouts under load. A quick patch (adding a retry mechanism) would temporarily solve visible errors but the fundamental architecture was flawed. The proper fix required refactoring to asynchronous calls with Redis caching and database connection pooling - estimated 12-14 days of work. My dilemma: the quick patch would make me look like a hero immediately and secure my PPO (Pre-Placement Offer) which was just 3 weeks away, but it would be a technical debt bomb for the team. The proper fix would take longer, risk annoying my manager with timeline delays, and might not be completed before my PPO evaluation. As an intern with no leverage, I felt pressure to just do what I was told (Task). I decided to be completely transparent and present a technical case to my manager. I created a detailed document with four sections: (1) Root cause analysis with code snippets and flow diagrams showing the synchronous bottleneck, (2) Quick patch solution with pros (2-day fix, immediate relief) and cons (doesn't scale beyond 5000 restaurants, will fail again at 20% load increase, creates technical debt), (3) Proper solution with architecture diagrams, implementation timeline of 13 days, and benefits (scales to 50,000+ restaurants, 40% faster API response, eliminates future incidents), and (4) Hybrid approach - implement quick patch in 2 days to stop immediate bleeding, then spend next 12 days on proper fix with feature flag for gradual rollout. I presented this in a 30-minute meeting with my manager and the team lead, backed with data from similar refactoring case studies from Swiggy's internal wiki. I explicitly said, 'I know my PPO evaluation is in 3 weeks and the quick fix would be safer for me personally, but I believe the hybrid approach is right for the team's long-term health. I'm willing to work evenings and weekends to deliver both' (Action). My manager was initially surprised that an intern was challenging his 2-day timeline, but after reviewing my technical analysis, he appreciated the thoroughness. He approved the hybrid approach and assigned a full-time SDE to pair-program with me on the refactoring. I implemented the quick patch in 1.5 days (not 2), deploying it on Friday afternoon. API failures dropped from 15% to 2%. Then I spent the next 10 days (working some late nights by choice) on the proper refactor. We deployed it with a feature flag to 10% traffic, gradually increasing to 100% over 5 days. The results: API failures dropped to 0.3%, average response time improved from 850ms to 510ms (40% improvement), and the system handled Swiggy's festival sale surge of 30,000 new restaurant registrations in one weekend without a single timeout. During my PPO evaluation, my manager specifically highlighted this as a case study of 'thinking beyond immediate tasks' and 'engineering maturity unusual for an intern.' I received a PPO at ₹14 LPA (above the average intern PPO of ₹11 LPA), and the team lead offered me a return full-time role in his team. More importantly, 4 months after I joined full-time, the restaurant onboarding system I refactored became a reference architecture that 3 other teams adopted. I learned that doing the right thing technically, even when it's riskier politically, earns long-term respect. I also learned to always present solutions, not just problems, and to back recommendations with data, not opinions (Result).",
        "key_points": [
            "Analyze root cause deeply, don't just fix symptoms",
            "Present technical decision with data-backed document (root cause, 3 solution options with pros/cons)",
            "Acknowledge personal risk openly (PPO evaluation) while recommending right solution",
            "Propose hybrid approach that balances short-term urgency and long-term quality",
            "Demonstrate ownership by offering extra effort (evenings/weekends)",
            "Quantify everything (15% failures, ₹8L daily loss, 850ms to 510ms, 40% improvement, 30K restaurants, ₹14 LPA PPO vs ₹11L average, 5-week internship, 3-week PPO timeline, 4-month impact)"
        ]
    },
    {
        "question": "You're in the HR round at Infosys (final round). The interviewer asks 'Why should we hire you over 200 other students from your college?' You're from a tier-3 college, have a 7.2 CGPA (not exceptional), no competitive programming medals, and one internship. How do you answer convincingly?",
        "expected_answer": "In the final HR round of Infosys campus placement at my tier-3 engineering college in Tamil Nadu, I faced Ms. Priya, an HR manager with 12 years of experience who had already interviewed 180 students that day (Situation). She asked directly, 'Your CGPA is 7.2, which is average in your batch. You don't have competitive programming achievements like several other candidates. Your internship was at a small local company, not a big brand. We're hiring only 25 out of 220 students. Why should you be one of them?' This was a make-or-break moment. I couldn't claim technical superiority over 9+ CGPA students or impressive brand names on my resume. I had 2-3 minutes to convince her I was worth the offer letter (Task). I took a 3-second pause to collect my thoughts, made direct eye contact, and gave a structured response. I started with radical honesty: 'You're absolutely right, Ma'am. I don't have the highest CGPA or big brand names. But let me share what I do have that makes me valuable to Infosys specifically.' I then structured my answer into four concrete points with specific examples. First, I spoke about consistent learning and adaptability: 'In my 6-month internship at a 15-person startup in Coimbatore, I was hired as a Java developer but the company pivoted to a React Native mobile app project. Instead of saying that's not my job, I self-learned React Native in 3 weeks using free resources, built the entire customer-facing app with 12 screens, and delivered it 4 days before deadline. That app is now used by 2,500+ local businesses for inventory management. This taught me that in the tech industry, your skill tags from Day 1 don't matter - your ability to learn what's needed does. At Infosys, you rotate employees across projects and technologies. My adaptability is my strength.' Second, I highlighted problem-solving in constraints: 'Coming from a tier-3 college, I didn't have access to premium courses or mentors. So I built my own study group of 6 students, organized weekend mock interview sessions, created a shared Google Doc with 500+ interview questions we collectively solved, and we taught each other data structures through peer learning. Out of my study group, 4 of us have cleared to this final HR round today. This shows I don't wait for perfect resources - I create solutions with what I have. Infosys values resourcefulness in client projects, and I've demonstrated that.' Third, I emphasized reliability and ownership: 'During my final year project, our team lead dropped out 40 days before submission due to personal issues. I was the only member who had full visibility of all modules. I took ownership, redistributed work, personally coded 15 extra hours over 2 weeks, and we submitted on time with zero plagiarism. We scored 88/100. Infosys's clients depend on timely delivery - I've proven I deliver under pressure without making excuses.' Fourth, I connected it specifically to Infosys: 'I researched Infosys's business model - you train freshers for 3-4 months and then deploy them to client locations. You're not looking for Day 1 experts; you're looking for people who are trainable, reliable, and professional. My 7.2 CGPA shows I'm consistent across 4 years, not brilliant in one semester and poor in another. Consistency matters for 2-year service agreements. I'm from a middle-class family - this job means my younger sister's education and our home loan EMI. I will not take this lightly or switch jobs in 6 months like some high CGPA students do after using Infosys as a backup. You're investing ₹2 lakh in my training - I will give you at least 2 years of committed service and ROI.' I concluded: 'Ma'am, I might not be the smartest candidate in the room today. But I'm definitely among the most committed, adaptable, and reliable ones. That's why I should be one of your 25' (Action). Ms. Priya's expression changed during my answer. She noted down several points and asked a follow-up: 'Tell me more about that React Native project.' I showed her the app on my phone (I had come prepared with it installed). The interview lasted 12 minutes instead of the usual 6. Two days later, results came out - I was one of 23 students selected (not 25; 2 positions were cancelled). My offer letter was for ₹3.6 LPA. Three of my study group friends also got offers. At Infosys's joining, during the orientation, Ms. Priya remembered me and said, 'Your answer about building your own study group showed initiative - that's rare.' I completed my training with 92% scores, was deployed to a banking client project in Pune, and after 18 months, received a 15% hike for excellent performance. The key lessons: When you can't compete on credentials, compete on character and specific evidence; Always connect your answer to the company's specific needs, not generic statements; Tell stories with numbers, not adjectives; And finally, honesty combined with self-awareness is powerful - don't fake what you don't have, showcase what you do have compellingly (Result).",
        "key_points": [
            "Acknowledge reality honestly instead of defending weaknesses",
            "Structure answer with 3-4 specific examples, not generic claims",
            "Demonstrate adaptability with concrete learning examples (Java to React Native in 3 weeks)",
            "Show problem-solving in resource-constrained environments (tier-3 college context)",
            "Prove reliability and ownership with project crisis example",
            "Connect explicitly to company's business model and needs (Infosys's fresher training approach, 2-year agreements)",
            "Quantify everything (7.2 CGPA, 220 candidates, 25 positions, 6-month internship, 2,500+ app users, 4/6 study group cleared, 88/100 project score, ₹3.6 LPA offer, 92% training scores, 15% hike, 18 months tenure)"
        ]
    },
    {
        "question": "During your technical interview at Amazon, the interviewer asks you to design a system like BookMyShow. You've never done system design before - your college didn't teach it. You have 45 minutes. How do you approach this without looking completely clueless?",
        "expected_answer": "In my final year, during Amazon's on-campus placement drive at my college in Delhi, I cleared the online assessment and two coding rounds (Situation). In the third round (system design), a senior engineer asked me to 'Design a ticket booking system like BookMyShow that can handle 10 million users booking tickets for 5,000 theaters across India.' I immediately panicked internally - our college curriculum covered data structures, algorithms, and some DBMS, but never high-level system design. Most students in tier-2/tier-3 colleges don't get this training. I had watched maybe 2-3 YouTube videos on system design but never designed a full system. I had 45 minutes to not look like a fool in front of an L5 engineer who designs systems daily. My goal wasn't to give a perfect answer (impossible with my experience) but to demonstrate structured thinking, ask smart questions, and show learning ability (Task). I took a deep breath and started with honesty: 'I want to be transparent - we didn't have a system design course in my curriculum, but I've read some blogs and I'll do my best to approach this structurally. Please feel free to guide me if I'm going in the wrong direction.' This set expectations and showed self-awareness. Then I broke down my approach into clear steps, asking clarifying questions at each stage. Step 1 - Requirements Gathering (5 minutes): Instead of jumping to solutions, I asked: 'Can I clarify the functional and non-functional requirements?' I listed functional: users can search movies, view available seats, book tickets, make payments, receive confirmations; and non-functional: 10M users, 5K theaters, what's the expected latency - 2 seconds for search?, high availability needed?, is it India-only or global? The interviewer was impressed I started with questions and said 'Good, most candidates start drawing boxes immediately.' He specified: focus on booking flow, assume 100K concurrent users during Friday night shows, and 99.9% availability. Step 2 - Back-of-envelope calculations (7 minutes): I said, 'Let me estimate the scale.' I wrote: 10M users, assume 5% book in a day (realistic?) - that's 500K bookings/day. Peak hours Friday 6-9 PM, assume 30% of daily bookings in 3 hours - that's 150K bookings in 3 hours = 14 bookings per second. But during big movie releases like Shah Rukh Khan films, could spike to 100 bookings/second. Average ticket booking: movie details (100 bytes), seat info (200 bytes), user data (200 bytes) = ~500 bytes per booking. 500K bookings/day = 250 MB/day, ~90 GB/year. I asked, 'Does this math make sense?' He said yes and noted that I was estimating traffic and storage. Step 3 - High-Level Design (15 minutes): I drew on the whiteboard: User → Load Balancer → Application Servers → Database. I explained: Load Balancer distributes traffic. App servers handle business logic (search, booking, payment). Database stores movies, theaters, seats, bookings. Then I added components: Cache (Redis) for movie listings and seat availability to reduce DB load. Message Queue (Kafka) for booking confirmations and email notifications. CDN for movie posters and static content. Payment Gateway integration (Razorpay/PayU). I explained each choice briefly. Step 4 - Deep dive on booking flow (13 minutes): The interviewer asked, 'Focus on the booking flow - when User A selects seats 12, 13 for a show, how do you ensure User B doesn't book the same seats simultaneously?' This is the classic concurrency problem. I said, 'This is where I'm uncertain, but here's my thinking: Option 1 - Database row-level locking: when User A selects seats, lock those rows in the database. Problem: if User A selects but doesn't pay, seats are blocked. Option 2 - Temporary reservation: when User A selects seats, mark them 'reserved' with a 10-minute timer. If not paid in 10 minutes, release seats. This is what I've noticed on BookMyShow. Option 3 - Optimistic locking with versioning. I'm not fully confident how this works in practice.' The interviewer smiled and said, 'Option 2 is the practical approach. How would you implement the 10-minute timer?' I said, 'Store seat reservation with timestamp in database or cache. A background cron job runs every minute to check and release expired reservations. Or use Redis TTL (Time to Live) feature to auto-expire.' He said, 'Good, Redis TTL is efficient. What about database choice?' I said, 'For theater/movie data, PostgreSQL or MySQL (relational) because data has clear schema. For user sessions or seat reservations, Redis (in-memory) for speed. For analytics like most booked movies, maybe a data warehouse later.' Step 5 - Bottlenecks and improvements (5 minutes): I asked myself aloud, 'Where could this fail?' I identified: Database could be a bottleneck - solution: read replicas for search queries, master for writes. Single point of failure - solution: deploy app servers in multiple availability zones. Payment gateway timeout - solution: async payment processing with queue. I mentioned I'd monitor with tools like Datadog (though I'd only heard the name). The interview ended. I said, 'I know I didn't cover everything like microservices architecture or detailed database schemas, but I tried to think through the core problems systematically' (Action). Two days later, I got the result - I was selected for the next round and eventually received an Amazon SDE-1 offer at ₹28.5 LPA. In the feedback session, the interviewer told me, 'You didn't have perfect system design knowledge, but you showed problem-solving structure, asked good clarifying questions, estimated scale, and admitted when you didn't know something instead of bluffing. That's what we look for in freshers - learning ability and structured thinking, not perfection.' At Amazon, I took internal system design courses and within 6 months was contributing to design discussions. The key lessons: When you don't know something, structured thinking beats fake expertise; Always start with clarifying questions - it buys you time and shows thoughtfulness; Break complex problems into smaller steps (requirements, calculations, design, deep dive, bottlenecks); Admit knowledge gaps honestly but attempt logical reasoning; And for college students - if your curriculum doesn't teach system design, watch YouTube channels like Gaurav Sen, System Design Interview, and read blog posts from real companies (Result).",
        "key_points": [
            "Start with honest acknowledgment of knowledge gaps, setting realistic expectations",
            "Ask clarifying questions before jumping to solutions (functional/non-functional requirements)",
            "Perform back-of-envelope calculations to show quantitative thinking (500K bookings/day, 14/sec, storage estimates)",
            "Use structured approach: requirements → calculations → high-level design → deep dive → bottlenecks",
            "Explain your reasoning for each component choice (Redis for caching, why, Kafka for queues)",
            "Identify and address the core technical challenge (seat booking concurrency)",
            "Admit when uncertain but provide logical alternatives (3 approaches to seat locking)",
            "Quantify everything (10M users, 5K theaters, 100K concurrent, 99.9% availability, 10-min timer, ₹28.5 LPA offer, 6 months to proficiency)"
        ]
    },
    {
        "question": "Your close friend from the same college is also sitting for the Google interview. You had your technical round in the morning and one specific LeetCode Hard problem was asked. Your friend's interview is in the afternoon. He texts asking 'How was it? What did they ask?' What do you reply?",
        "expected_answer": "During final year Google placement drive at IIT Bombay in October, both my friend Arjun and I cleared the resume shortlisting for SDE intern roles (Situation). Interview slots were assigned randomly - mine was 10 AM and his was 3 PM on the same day. We'd been practicing together for 4 months, had shared a joint LeetCode subscription, and he'd helped me debug my projects multiple times. We were close friends who'd supported each other through tough semesters. In my 10 AM interview, the interviewer asked me 'Median of Two Sorted Arrays' - a LeetCode Hard problem that requires binary search optimization for O(log(min(m,n))) complexity. After the interview, I went to the canteen and at 12:30 PM, Arjun texted me: 'Bro, how did it go? What kind of questions? Any specific topics?' I knew exactly what he was asking - he wanted to know the specific problem so he could prepare the solution before his 3 PM slot. This happens commonly during campus placements when multiple students interview the same day (Task). I faced a serious ethical dilemma. On one hand, Arjun was my closest friend, had genuinely helped me throughout college, and I wanted him to succeed. Sharing the problem would significantly increase his chances - he could study the solution, understand the approach, and ace his interview. Many students do this during campus placements; it's an unwritten practice. If I didn't help him and he failed, he'd feel betrayed. Moreover, what if he finds out I knew the question and didn't share it? Our friendship could be damaged. On the other hand, I was painfully aware this was cheating and violated interview integrity. Google explicitly tells candidates 'Do not discuss interview questions with anyone.' If Arjun got selected purely because of my help and I knew it, I'd feel complicit. More importantly, if Google found out through their systems (they track which problems are asked to which candidates and their solutions), both of us could be blacklisted, not just from this interview but future Google opportunities. Additionally, from a practical career standpoint, if Arjun got the job based on memorizing one problem I shared, he'd struggle in the actual role when faced with real problems, which wouldn't help his long-term career. Finally, I had to ask myself: what kind of professional did I want to be? The easy choice was help my friend; the right choice was maintain integrity. I decided integrity mattered more than short-term friendship comfort (Task clarification). I replied to Arjun within 10 minutes: 'Hey bro, interview went okay but tough. I can't share specific questions - Google's NDA is strict and they track this stuff. I don't want to risk getting both of us in trouble. But I can tell you this - focus on binary search optimizations and edge case handling. They care a lot about communication and explaining your thought process, not just correct code. Make sure you ask clarifying questions before coding. You've got this man, you've been practicing hard. Trust your prep 💪' After sending this, I immediately called him. On the call, I said, 'I know you wanted the specific question and I get it. But think about it - even if you ace one question because I told you, what happens in the next rounds or on the actual job? You're smart enough to clear this on your own prep. I can't compromise your long-term by giving short-term help that's cheating. I value our friendship more than to set you up for failure by making you dependent on leaks.' Arjun was silent for a few seconds. Then he said, 'You're right bro, I was stressed and asked without thinking. Thanks for not letting me make that mistake. I'll trust my preparation.' We talked for 10 more minutes where I gave him genuine tips: stay calm, use the whiteboard clearly, and remember Google cares about problem-solving approach more than perfect syntax (Action). At 6 PM, Arjun called me - he'd cleared his interview. His problem was different from mine (it was 'Longest Increasing Subsequence'). He said, 'Glad I relied on fundamentals and not shortcuts.' We both cleared all rounds. I received a Google SDE intern offer at ₹1.5 lakh/month stipend (₹9 LPA if converted), and Arjun got the same. We interned at Google Bangalore the following summer. During the internship, I told Arjun about my internal conflict that day. He thanked me and said, 'If you'd helped me cheat, I'd always have doubted my own ability. You did the right thing.' Three years later, both of us are full-time at Google (I'm SDE-2 now at ₹45 LPA, he's SDE-2 at Google Cloud). We still have a strong friendship built on mutual respect and integrity. More importantly, during our time at Google, we've encountered many situations requiring ethical judgment - in code reviews, in handling user data, in reporting bugs that could delay launches. That placement interview moment taught both of us that integrity isn't situational. The key lesson: Real friends don't help each other cheat; they help each other build skills. Short-term help through shortcuts creates long-term dependency and self-doubt. And professionally, one compromise of integrity makes the next compromise easier - it's a slippery slope. Your reputation is built on hundreds of small choices where no one's watching (Result).",
        "key_points": [
            "Recognize the ethical dilemma clearly: friendship loyalty vs. professional integrity",
            "Refuse to share specific questions while still being supportive with general guidance",
            "Explain the risk to both parties if discovered (blacklisting, reputation damage)",
            "Help friend understand that short-term 'help' hurts long-term capability building",
            "Offer alternative support (general tips, encouragement, call to reduce anxiety)",
            "Follow up personally to explain reasoning and preserve friendship",
            "Quantify outcomes (both cleared, ₹1.5L/month internship, ₹9 LPA conversion, ₹45 LPA current, SDE-2 level, 3 years career impact)",
            "Emphasize principle: integrity in small moments defines professional character"
        ]
    }
]
# --- End Questions Bank ---

current_question = None
logs = []  
# --- 3. LOAD AI MODELS ---

# --- 3. LOAD AI MODELS ---
print("\n" + "="*50)
print("CHECKING AVAILABLE GEMINI MODELS")
print("="*50)
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("\nAvailable models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  ✓ {model.name}")
    print()
except Exception as e:
    print(f"⚠️  Error: {e}\n")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    llm_model = genai.GenerativeModel('gemini-2.0-flash')
    print("✅ Gemini configured: gemini-2.0-flash\n")
except Exception as e:
    try:
        llm_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print("✅ Gemini configured: gemini-1.5-flash-latest\n")
    except:
        llm_model = None

print("="*50)
print("LOADING WHISPER STT MODEL")
print("="*50)
try:
    stt_model = whisper.load_model("base")
    print("✅ Whisper loaded\n")
except Exception as e:
    stt_model = None

print("="*50 + "\n")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- Helper Functions ---
def analyze_fillers(transcript):
    FILLER_WORDS = ['um', 'uh', 'like', 'you know', 'so', 'ah', 'actually', 'basically']
    report = {}
    words = transcript.lower().split()
    for filler in FILLER_WORDS:
        count = words.count(filler)
        if count > 0:
            report[filler] = count
    return report

def analyze_star_with_gemini(transcript, expected_answer, key_points):
    if not llm_model:
        return {"score": 3, "feedback": "Gemini not configured."}
    
    points_str = "\n".join([f"- {point}" for point in key_points])
    
    prompt = f"""Evaluate this student's campus placement interview answer.

EXPECTED ANSWER:
"{expected_answer}"

KEY POINTS:
{points_str}

STUDENT'S ANSWER:
"{transcript}"

Return ONLY valid JSON (no markdown):
{{"score": 3, "feedback": "specific advice"}}

Score 1-5 based on how many key points covered."""
    
    try:
        response = llm_model.generate_content(prompt, request_options={'timeout': 20})
        if not response or not response.text:
            return {"score": 3, "feedback": "Empty response"}
        
        json_text = response.text.strip().replace("``````", "")
        start = json_text.find('{')
        end = json_text.rfind('}')
        if start != -1 and end != -1:
            json_text = json_text[start:end+1]
        
        return json.loads(json_text)
    except:
        return {"score": 3, "feedback": "Analysis completed."}

# --- API Routes ---

@app.route('/')
def home():
    """Serve the HTML page"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/get-question', methods=['GET'])
def get_question():
    global current_question, logs
    current_question = random.choice(INTERVIEW_QUESTIONS)
    logs.append(f"📋 Question loaded at {datetime.now().strftime('%H:%M:%S')}")
    print(f"✅ Question sent: {current_question['question'][:50]}...")
    return jsonify({
        "question": current_question['question'],
        "expected_answer": current_question['expected_answer'],
        "key_points": current_question['key_points']
    })

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Return recent logs for display on webpage"""
    return jsonify({"logs": logs[-20:]})

@app.route('/api/analyze', methods=['POST'])
def analyze_audio():
    global current_question, logs
    
    logs.append(f"📁 Audio file received at {datetime.now().strftime('%H:%M:%S')}")
    
    if not stt_model:
        logs.append("⚠️  Whisper model not loaded!")
        return jsonify({"error": "Whisper not loaded"}), 500
    
    if 'audioFile' not in request.files:
        logs.append("⚠️  No audio file in request")
        return jsonify({"error": "No audio file"}), 400
    
    audio_file = request.files['audioFile']
    audio_path = os.path.join(UPLOAD_FOLDER, 'temp_audio.webm')
    
    try:
        audio_file.save(audio_path)
        logs.append(f"💾 Audio saved: {audio_path}")
    except Exception as e:
        logs.append(f"⚠️  Error saving file: {e}")
        return jsonify({"error": str(e)}), 500
    
    transcript = ""
    try:
        logs.append("🎤 Transcribing audio with Whisper...")
        result = stt_model.transcribe(audio_path)
        transcript = result["text"]
        logs.append(f"📝 Transcript: {transcript[:80]}...")
        print(f"📝 Transcript: {transcript}")
    except Exception as e:
        logs.append(f"⚠️  Transcription error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logs.append("🗑️  Temporary file deleted")
    
    if not transcript:
        logs.append("⚠️  Empty transcript")
        return jsonify({
            "transcript": "[Could not understand audio]",
            "fillerWords": {},
            "starAnalysis": {"score": 0, "feedback": "No audio detected"}
        })
    
    logs.append("🔍 Analyzing filler words...")
    filler_report = analyze_fillers(transcript)
    logs.append(f"Found {len(filler_report)} types of filler words")
    
    logs.append("🤖 Sending to Gemini for STAR analysis...")
    star_report = analyze_star_with_gemini(
        transcript,
        current_question['expected_answer'],
        current_question['key_points']
    )
    logs.append(f"✅ Analysis complete! Score: {star_report.get('score', 0)}/5")
    
    return jsonify({
        "transcript": transcript,
        "fillerWords": filler_report,
        "starAnalysis": star_report
    })

# --- Run ---
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 AI INTERVIEW COACH - CAMPUS PLACEMENT EDITION")
    print("="*50)
    print("Server URL: http://127.0.0.1:5000")
    print("Loaded 3 placement-focused scenario questions")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)