# The Scoreboard That Didn't Count

**What happened when I let AI agents run three months of research in two fields
I knew nothing about.**

I spent the summer of 2026 competing in two artificial-intelligence contests I
had no business entering. I am not a security researcher. I am not an AI
researcher. I have spent sixteen years as a consultant and architect, building
decisioning systems for companies, and my own coding had gone rusty enough that
most of the Python I had written in recent years was written with help.

So I did the obvious modern thing: I let AI coding agents do the work. I gave
one of them an instruction I have thought about a lot since — "continue to work
in loops and iterations until you solve the challenge" — and then I watched what
happened, kept a careful record of every decision, and tried to be honest about
the results.

The short version: the agents were remarkable. They also could not do science.
Those two sentences are not in tension, and the space between them is the most
useful thing I learned.

---

## The two contests

The first was about breaking AI assistants. Modern assistants can browse, send
email, write files, and call other software. That power creates a security
problem: can someone trick an assistant into misusing its own tools? The contest
gave you a sandboxed assistant and a scoring system, and asked you to find ways
to make it misbehave — smuggling out a secret, say, or being talked into sending
something it shouldn't. Four thousand teams entered.

The second, ARC-AGI-3, was almost the opposite. It gives an AI a small video
game it has never seen, with no instructions, and asks it to work out the rules
by playing. Humans find these easy. Machines find them very hard. Nearly three
thousand teams entered that one.

I picked two fields I didn't understand on purpose. If agents really lower the
barrier to technical work, that is exactly where you'd see it.

---

## What the agents were genuinely good at

I want to be fair before I am critical, because the critical part gets more
attention and it would be easy to leave the wrong impression.

The agents read unfamiliar codebases faster than I could have and turned them
into something I could act on. They found the contest's own scoring code and
worked out what it actually rewarded, which is different from what the
documentation said it rewarded. When a software update silently broke my
submissions, an agent found the cause — the scorer had started demanding a
specific marker in the data, and my older attacks no longer carried it — and
fixed it in an afternoon. That kind of plumbing sounds unglamorous. It was the
difference between competing and not competing.

They built instruments, too. In the games contest, an agent measured how much
the score wobbled between two runs of *identical* code, so I would know how big
a difference had to be before it meant anything. That number turned out to
matter enormously, and I'll come back to it.

And they were tireless in a way I am not. They ran hundreds of experiments
overnight, kept records, and never got bored of a dead end.

If the question is "can these tools let a competent outsider do real technical
work in a field they don't know," my answer is an unambiguous yes. I finished
just inside the top five percent of a four-thousand-team security contest. I could not
have done that alone.

But that question turns out to be much smaller than it sounds.

---

## The scoreboard that didn't count

Here is the thing I did not see coming.

Contests like this have two scoreboards. There is a public one that updates
while you compete, and a hidden one, scored on problems you never see, that
decides who actually wins. Everyone knows this. Everyone says they know this.

For nearly three months, my agents and I optimized the public scoreboard. It was
right there. It responded to changes. It gave us a number to chase, and we
chased it — measuring how fast the system could process our attacks, packing
more of them into each submission, shaving fractions of a second off the
machinery. We got the public score up to 92.7 and spent weeks trying to push it
further.

When the contest closed and the hidden scoreboard was revealed, I pulled every
submission I had ever made. Fifty of them. Forty-nine had been scored.

**Thirty-eight of those forty-nine scored exactly zero.**

Not "scored badly." Zero. Including our best public submission, the 92.7 we had
worked toward for months. It was worth nothing at all.

Eleven submissions scored something. Every single one came from a completely
different line of work — a small side bet, made because I was uneasy about
putting everything on one strategy, that tried a different kind of attack
entirely. Instead of smuggling data out directly, it talked the assistant into
using its own email tool to do the sending. That side bet never scored above
16.6 on the public board. On the hidden board it was the only thing I had that
scored at all.

I want to be careful about what this proves. It is one competitor's fifty
submissions, not a law of nature, and I still don't know exactly why the hidden
scorer behaved that way. But as a description of my own three months it is
brutally clear: almost everything the agents and I optimized was measured
against the wrong target, and the thing that saved the result was a hedge I made
out of unease rather than evidence.

The agents never suggested that hedge. They were extremely good at climbing the
hill in front of them. Not one of them ever asked whether it was the right hill.

I finished 171st out of 4,186 — a silver medal. The notification I received said
173rd of 4,251, a small discrepancy I was never able to reconcile, and I've left
both numbers in rather than quietly picking the nicer one.

---

## The competition where I did better by copying

The games contest went differently, and the difference is instructive.

For two months my score crawled. Every improvement my agents and I invented
moved it a little — a tenth of a point here, four hundredths there. The best
in-house result after all that work was 1.94.

Then, in early September, I did something that felt like giving up. Another
competitor had published their notebook — their entire working solution, in
public, for anyone to read. I copied it. Not adapted, not learned from: copied,
byte for byte, and submitted it under my own name with the source named in the
submission.

It scored 3.25.

One act of copying beat every original idea we'd had in two months, combined and
then some. Nothing my agents originated ever moved that score by more than
0.44. The copy moved it by 1.31.

Everything I flew afterwards, including the 4.31 that briefly put me 26th out of
2,892 teams, is that same borrowed notebook with a single setting changed.

There is nothing improper here — the notebook was published for others to use,
and I named it every time. But I want to sit with what it means rather than move
past it. The single most successful thing that happened in three months of
agent-assisted research was recognizing that someone else had already done it
better. That is a real skill. It is not the skill the technology is usually sold
as having.

---

## The ruler that wouldn't hold still

Then came the part that made me question everything that came before it.

Curious about how much of my score was real, I submitted the *identical file*
three times. Same code, same settings, nothing changed.

It scored 3.25, then 2.58, and the third attempt failed outright with a platform
error.

I tried it again with the one-setting variant. That returned 4.31, then 2.45,
then 4.01.

Read that again, because it took me a while to absorb. Unchanged code produced
scores ranging from 2.45 to 4.31. Which means that most of the "improvements" I
had spent two months carefully measuring — the tenth of a point here, the four
hundredths there — were not improvements. They were noise. I had been reading
tea leaves and writing down what I saw.

That one 4.31, the score that put me 26th, was the luckiest draw of a wobbly
instrument. I have not pretended otherwise anywhere in my write-ups, and I'd
encourage anyone reading a leaderboard to ask the same question I failed to ask
for two months: how much does this number move when nothing changes?

---

## Confidently wrong

The failures that worried me most were not the ones where an agent got a wrong
answer. They were the ones where it got a wrong answer with complete confidence,
and I only caught it because I happened to ask.

The clearest example: an agent fine-tuned a model, tested it, and reported that
the tuned version beat the original. The numbers looked good. The agent was
sure. Something made me ask it to prove which model had actually been running
during the test.

The tuned model had never loaded. Both sides of the "comparison" were the same
original model. The experiment hadn't produced a weak result — it had produced
no result at all, and would have gone into my records as a success if I hadn't
asked an awkward question at the right moment.

That was not a one-off. An agent explained one model's poor performance as the
model being weak, when in fact the test was set up badly enough that the *other*
model also scored zero under it. Another built an elaborate multi-branch
experiment where the branches all changed several things at once, so no result
could ever tell us which change mattered.

None of these are stupid mistakes. They are the mistakes of something that is
fluent in the form of science without being accountable to its substance. An
agent will produce a well-structured experiment, a confident summary, and a
clean conclusion whether or not the underlying test can support any of it. The
output looks identical either way. That is the part I find genuinely hard to
work with.

When I logged all 38 decision points across both contests, the pattern was
plain. Eight propositions survived scrutiny. Ten were partly supported. Ten were
refuted outright. Five turned out to be experiments that couldn't have answered
their own question. The agents generated no shortage of ideas. Choosing between
them, and knowing when one had been properly tested, was where things fell down.

---

## What actually worked

Looking back, almost everything that saved me from a worse result was a habit
rather than a technology.

**Deciding the rule before seeing the number.** Late in the games contest I
started writing down, before running an experiment, exactly what result would
count as success and what would count as failure. It sounds bureaucratic. It is
the single most valuable thing I did. One promising change engaged perfectly —
it altered the agent's behavior exactly as designed, visibly, measurably — and
produced no improvement at all. Because I'd fixed the threshold in advance, I
recorded it as a failure and moved on. Without that rule I am confident I would
have talked myself into keeping it, because the mechanism so obviously *worked*.

**Asking what is actually running.** After the fine-tuning incident, "prove
which model is serving before we interpret anything" became a standing rule. It
caught problems more than once.

**Keeping the failures.** I kept a record where refuted results, invalid
experiments and unresolved ones stayed visibly different from each other. It is
tempting to compress a project into the story of what worked. Doing so quietly
destroys the information you need most.

**Treating the agent's memory as claims, not facts.** Agents carry conclusions
forward between sessions. Some of those conclusions were wrong when they were
written and got more confident with age. At one point I brought in a completely
different system and told it not to trust any of the recorded conclusions and to
verify everything from scratch. That found real problems.

None of these are clever. All of them are the kind of discipline that a
researcher would call basic and that an agent, left alone, will not supply.

I estimate I spent two to five hours a day on this — reading claims, demanding
better tests, redirecting work, deciding what was allowed to proceed. That is
not supervision. That is a job.

---

## What I'd tell you

If you are thinking about pointing these tools at real work, three things.

**They collapse the barrier to entry, and that is not a small thing.** I did
work in two unfamiliar technical fields that would otherwise have been closed to
me, and I learned a great deal doing it. If you have been waiting for permission
to try something technically ambitious, this is as good as that permission has
ever been.

**They will not tell you that you are solving the wrong problem.** Every agent I
used was excellent at making the number in front of it go up. Not one ever
asked whether that number was the one that mattered. That judgment stayed mine
the entire time, and the one time it mattered most, I got it right by
accident — out of unease rather than analysis.

**Fluency is not reliability, and they look the same.** A confident, well-
organized, clearly-written wrong answer is the characteristic failure of this
technology. You cannot catch it by reading the output more carefully, because
the output is not where the flaw is. You catch it by asking what was actually
tested, what was actually running, and what result would have changed your mind.

---

## What this isn't

One person, two contests, one summer. There is no control group — I have no idea
what I'd have achieved without the agents, and anyone who tells you they can
measure that from a study like this is guessing. I chose these cases because
they are mine, which means I chose what to write about. I coded my own records,
so my interpretation is in them. Contest scores measure contest performance, not
scientific quality. And I spent roughly a hundred dollars on one AI service and
thirty on another, plus subscriptions I didn't track carefully enough to report.

I also want to be straight about the outcome. I did not win either contest. The
silver medal was a good result and it was not a win, and the games contest was
still running when I wrote this, sitting on a borrowed notebook and a lucky
draw.

What I have is not proof of anything general. It is a detailed, honest record of
what happened, with the failures left in.

The most useful sentence I can leave you with is the one I opened with. The
agents were remarkable, and they could not do science. They executed nearly
everything I asked and judged almost nothing well. Every piece of value I got
came from the part where a human decided what was worth doing, what counted as
evidence, and when to stop.

That part has not been automated. On this evidence, it isn't close.

---

*The full research paper behind this case study, with the complete evidence
record, submission-level data, and the coding of all 38 decision points, is
available as* Access Without Autonomy: An Instrumented Case Study of AI Agents
in Computational Research.
