# Technical Debt: Experience, Thoughts and Strategies

Throughout my career, I've encountered a substantial amount of technical debt, a challenge that many in the software industry can relate to. Despite employing numerous methods and significant resources to tackle this issue, it remains an unavoidable part of our daily struggle. My recent experience with this "wild beast" was the trigger for this article. Without wasting more of your time, let's dive into the nature of technical debt and explore potential solutions to deal with it.


## The Nature of Technical Debt
While many compare technical debt to financial loans, this analogy is not quite right. To secure a loan, one must present assurances and undergo a thoughtful process (or at least should). Once the loan is acquired, there's a clear path to settling it. In contrast, technical debt often accumulates without explicit consent, and its origin has many sources, also its resolution is much more complex.

Technical debt, from my perspective, in its nature is very close to a pesky garden weed. Just as weeds persistently grow back and spread throughout a garden, technical debt re-emerges and proliferates through a codebase. Both demand regular attention to manage; leave them unchecked, and they can choke productivity, much like weeds competing with plants for nutrients. The root causes of weeds—be it external factors or poor maintenance—parallel the diverse origins of technical debt, such as rushed coding or outdated tech. However, with the right strategies, just as some weeds can be repurposed beneficially in gardening, technical debt can occasionally be leveraged strategically in development.

## The Roots of Technical Debt

### Communication: The Good, The Bad, and The Off-Topic
Ever found yourself in a standup, internally groaning, "Here we go again"? Moments when team members "passionately" share their daily updates; I did this... will work on that... no blockers... And you are left scratching your head about the project's actual progress. To make it even more engaging, someone chimes in with a topic about other task/discussion in some distant universe. And just like that, the essence of the standup evaporates.

Now, let me share a little secret with you - though you might've already sensed it. These meetings? They often don’t hold the value everyone assumes. When miscommunication runs the show, and teams aren't truly syncing, we're not just losing time. This disjointedness can ripple into technical misunderstandings, which might silently feed technical debt.

In the world of standups, brevity is brilliance. My experience taught me that the best standups are the ones where deliverables take the center stage. Dive deep into those user stories. Seek out feedback, flag those blockers, and set your gaze at that deployment goal. Let's skip the mundane daily play-by-plays; they often don't offer the insights or synchronicity we truly need.

Moreover, if your standup starts to resemble a random chat room, it's waving a big red flag. It's hinting at a deeper communication issue brewing during the rest of the day. Group your team, figure out what's pulling these off-course conversations into your standups. After all, these sessions are for the collective, not personal monologues.


### Disorganised Planning
Now, you opened your project tools and felt like you've stumbled into a forgotten storage room, instead of a neatly laid-out plan? Where the backlog resembles an old attic filled with cobwebs and long-forgotten memories? Then, you dart your eyes to the sprint board: it's a desert, barren of goals, sprinkled with last-minute ticket additions, and user stories that echo emptiness. And the standup updates? They seem to be telling tales from a different universe, entirely unlinked from the reality you see. The so-called "roadmap"? It's more like a mishmash of guesses and wishes, looking suspiciously like a compost heap rather than a well-paved path forward. Quite the adventure, isn't it?

Let be serious for a second, shall we? In such an environment the focus and essence is lost. Developers might find themselves investing time and skill into tasks that that end up being scrapped or might become obsolete tomorrow. Such discrepancies can lead to half-baked solutions or rushed code, fattening up our technical debt.

For optimal project flow, it's crucial to keep the team aligned with top-priority tasks. Clear sprint goals and well-defined user stories act as guides, steering developers effectively. During planning, present a clear vision, convey its value, and seek the team's insights, ensuring clarity and engagement.

### The Dilemma of Documentation: Too Much, Too Little, Too Scattered
Picture this: You're on a treasure hunt, but instead of a map leading you to the gold, you've got a mountain of papers, scattered across all the places, and you’re trying to find that one piece of critical information. Sounds exhausting, right? Now, swing to the other extreme: you're in that same hunt, but this time there's no map at all. You're blindfolded, relying on whispers and hunches. Neither scenario is particularly inviting, is it? 

Documentation in either of state, can slow down processes, lead to assumptions, or even encourage workarounds, all of which aren't best practices. So, what's the way forward? Think of documentation as of a craft, where less can be more, but clarity is king. Prioritise brevity, but ensure all critical information stands out. Discuss it, make sure everyone's on the same page. 

Real game changer here is to cultivate the culture where regularly reviewing and updating documentation is an integral part of a well-defined definition of done.


### Legacy Code Challenges: Nurturing New Features While Pruning the Old
Features are like plants in a flourishing garden, where vibrant, new flowers are vying for space, nutrients, and sunlight. Yet, there are older, wilting plants that have long passed their prime but still occupy valuable ground. As a gardener, you'd want to ensure that both the blossoming flowers and the matured plants coexist, but there comes a time when one must prune the old to make room for the new.

We want to be wise about what is a keeper and what not. Effective communication with the business side is crucial in such scenarios. Highlight the importance of phasing out outdated or no longer used features. During estimates include refactoring in your estimates. As you integrate new features, take the opportunity to clean up and remove any unnecessary or obsolete code. In your code utilise patterns like; strangler, adapter, facade, bridge, anti-corruption layer, etc. Favor incremental changes ensuring that the system remains stable at each step.


### Outdated Tooling and Libraries
Working with inadequate tools feels like using a hammer for everything in the garden. Sure, you can give that wonky fence a few extra nails, but when it comes to planting? Good luck with using hammer. And don't even get me started on the dangers of using a rusty, worn-out shovel – it's just asking yourself for troubles. 

In the tech realm, this scenario is more common than you'd think. Using outdated or ill-suited software is just like trying to garden with the wrong equipment. It can not only impede progress but also open up vulnerabilities. Just as a rusty shovel might harm us, outdated tools in our tech projects can leave us exposed to various pitfalls, slowing down progress and compromising security. I've witnessed this firsthand with issues like outdated TLS protocols and the cessation of support for once-popular frameworks. Often, developers, under pressure, resort to temporary workarounds rather than implementing optimal solution.

The solution; take a proactive approach by keeping a vigilant eye on the tools and libraries you use. Know their lifespans, and be aware of when they're nearing their end. Schedule a periodic 'tool check' and make it a habit to discuss the state of your tooling. Perhaps even set reminders or alarms – whatever it takes to ensure you don’t get caught off-guard. 

And during project planning? Make addressing these concerns part of your non-functional requirements. It might seem like extra work now, but trust me, future-you will be sending heaps of gratitude for the saved headaches and smoother sails.

### Low confidence in deliveries

Navigating a production environment teeming with uncertainty is something many of us have faced. Wrestling with broken artifacts, holding breath during a release or releasing with failing tests or no coverage, sound familiar? For those who haven't experienced this chaos, cast the first stone.

This isn't just about the palpable tension that fills the room during each deployment; it's the persistent, nagging doubt that shadows every decision. When teams constantly question the stability and reliability of what they're shipping, it not only affects morale but sows the seeds of technical debt.

Addressing this requires a foundational approach. Begin by scrutinizing the integrity of your CI/CD pipeline, ensuring it's more than just a series of checks. It's crucial that tests are meaningful, offering not just "green ticks" but real assurance. Encourage your team to understand the significance of tests. Don't focus on coverage numbers, focus on their quality during Pull Request reviews. Beyond assurance, they also serve as a form of documentation.

### Team Burnout

Tirelessly watering garden under a scorching sun has its limits. Pushing a team to work at maximum capacity without pause. Initially, there's a burst of productivity as everyone rises to the challenge. However, with time and without relief, that enthusiasm diminishes, and performance begins to suffer.

Burnout isn't merely about physical and mental fatigue. It's the overwhelming sensation of being trapped in an endless cycle, feeling as though you're perpetually running but not making progress. Overloading can lead to a rapid decline in quality and enthusiasm.

When setting your team's goals and timelines, the emphasis should be on long-term sustainability. Ensure pauses between demanding cycles, channel resources into skill development, and foster a culture where feedback is not just encouraged but expected. Keep an eye on the distribution of tasks: ensure members alternate between bug-fixes and feature developments. It's also essential that intense sprints are succeeded by more relaxed ones.

Recognizing and acting on burnout symptoms late in the game can have irreversible consequences. Not only do you risk the break of team efficiency, but trust, once lost, might be never regained again. 

## Harnessing Technical Debt to Your Advantage
While technical debt often gets a bad reputation, it can be harnessed strategically to provide a technical edge. When managed correctly, it can serve as a springboard for both growth and innovation. Moreover, it can bolster your team during demanding phases, offering a buffer that enables a more fluid development process.

Just as in gardening, where an excessive amount of compost can smother plants and hinder growth, unchecked technical debt can stifle your projects. It's all about understanding when and how to utilize it. Finding that balance is key to ensuring your 'tech garden' thrives and remains productive.

Let's explore some strategic approaches to employ technical debt as a beneficial tool rather than seeing it as a disastrous outcome of our actions.

### Steering Development with Iterative Enhancement

The term "Minimum Viable Product" or MVP has become somewhat of a buzzword in the software development industry. At its core, it represents a strategy to launch a product outfitted with just the essential features to captivate early users. Once it's out in the wild, the real work begins—gathering feedback and making iterative refinements. This approach is not just about speed; it's about ensuring that the enhancements resonate with genuine user needs and experiences.

The beauty of iterative development lies in its flexibility. By adopting this method, teams can make informed adjustments rooted in tangible user insights, ensuring that the product's evolution aligns seamlessly with user expectations. This approach enables teams to adapt to changes smoothly, instead of chasing an elusive 'perfect' first implementation.

However, MVP is a tool, and like any other tool, its success depends on how and where you deploy it. Implementing an MVP without a clear roadmap for subsequent stages or using it as a ready foundation for evolving product might quickly become a nightmare to maintain and scale. Communication and good planning here is the key to success.

### Secure a Competitive Edge

I find that there's a certain comfort in stability. Like many, I prefer the familiarity and security of my job and don't enjoy the constant chase for the next big thing (although sometimes it is inevitable, it might be a good topic for another article). Yet, ensuring the product we support remains competitive can often feel like a high-wire act, demanding strategic choices and sometimes sacrifices.

One such sacrifice is the conscious decision to incur technical debt. It's a calculated risk, much like a chess player sacrificing a piece to protect the king. By expediting feature releases or pushing out products quicker than the competition, we hope to seize a unique market position, even if it means incurring some short-term challenges.

Similarly to MVP, this strategy cannot be used recklessly. With careful planning, foresight, and regular debt repayments, it's possible to maintain that delicate balance between staying competitive and ensuring long-term sustainability.


### Planning on Taking a Breather

We've all had those days, and if you're thinking, "What days?", well, allow me to paint the picture. It's those times when the team's enthusiasm feels like it's on a low battery, faces looking as if they've read a hundred lines of faulty code, and that usual energetic buzz of getting things done is more like the hum of a computer on standby. And yet, the ticking clock doesn't halt, and the mountain of tasks seems to grow like an unchecked stack of notifications.

Now, the instinctive response might be to chug down another coffee, roll up the sleeves, and dive deep, hoping to emerge with a masterstroke solution. But sometimes, the best answer isn't in pushing the accelerator but in tapping the brakes. It might sound counterintuitive, but taking a short detour now, perhaps easing the work tempo or having a spontaneous team game session, can provide the needed breather. This isn't about negligence; it's strategic procrastination. Address that technical debt later when the spirits and energy levels are up.

By consciously scheduling these mini-recesses during grueling phases, we equip teams to recharge and re-emerge with renewed vigor and clarity. It's a simple truth: A rejuvenated team isn't just in better spirits, they're sharper, more cohesive, and innovative. So in the fast-paced rhythm of the tech domain, sometimes to move forward effectively, a brief pause is all we need.

## Summing it all up

I trust that this article shed light on a fresh perspective of technical debt. Far from being a mere adversary, it can sometimes act as an ally when wielded judiciously. Like many facets of the development lifecycle, technical debt isn't inherently good or bad; it's our approach and management of it that determines its impact.

Remember, technical debt isn't just the product of decisions made by a select few; it's collective. Every choice, every compromise, and every corner cut contribute to the growing ledger. It's not "their" problem or "his/her" mistake; it's a shared responsibility that echoes the voice of the entire team.

So, whether you're a developer deep in the trenches, a lead overseeing the broader strategy, or a product owner juggling priorities, it's essential to remain on guard. Embrace technical debt when it serves a strategic purpose, but always with a clear understanding of its implications. Use it not as a crutch, but as a calculated lever to propel projects forward, nourish team dynamics, and drive innovation.

Happy Coding!
