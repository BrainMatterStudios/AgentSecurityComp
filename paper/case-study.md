# The Reframe I Ignored

**My AI agents worked out the winning strategy in writing on the first of
August. I kept working on the wrong thing until the twenty-third.**

I spent the summer of 2026 competing in two artificial-intelligence contests I
had no business entering. I am not a security researcher. I am not an AI
researcher. I have spent more than sixteen years as a consultant and architect,
and my own coding had gone rusty enough that most of the Python I had written in
recent years was written with help.

So I did the obvious modern thing and let AI coding agents do the work. I gave
one of them an instruction I have thought about a lot since — "continue to work
in loops and iterations until you solve the challenge" — and then spent two to
five hours a day reading what came back, demanding better tests, and deciding
what was allowed to proceed.

I expected to learn that the agents couldn't think strategically. That is the
comfortable story, it is what most write-ups of this kind conclude, and when I
first drafted this piece it was what I wrote. Then I went back through my own
files and found that it wasn't true. The agents produced the correct strategic
call, in writing, weeks before it mattered. The person who failed to act on it
was me.

---

## The two contests

The first was about breaking AI assistants. Modern assistants can browse, send
email, and use other software on your behalf, which creates an obvious problem:
can someone trick one into misusing its own tools? The contest gave you a
walled-off assistant and asked you to find ways to make it misbehave. Four
thousand teams entered.

The second, ARC-AGI-3, was almost the opposite. It hands an AI a small video game
it has never seen, with no instructions, and asks it to work out the rules by
playing. Humans find these easy. Machines find them very hard. Nearly three
thousand teams entered.

I picked two fields I didn't understand on purpose. If agents really lower the
barrier to technical work, that is where you would see it.

---

## What the agents were good at

The agents read unfamiliar codebases faster than I could have and turned them
into something I could act on. They found the contest's own scoring code and
worked out what it actually rewarded, which is not the same as what the
documentation said it rewarded.

They built instruments. In the games contest an agent measured how much the
score wobbled between two runs of identical code — the beginning of a habit that
later saved me from a much more embarrassing mistake.

And they were tireless. They ran long batches unattended, kept records, and
never got bored of a dead end.

I finished just inside the top five percent of a four-thousand-team security
contest. It felt like something I could not have done alone, though I have no
control group, so that is a feeling and not a finding.

---

## The scoreboard that didn't count

Contests like this have two scoreboards: a public one that updates while you
compete, and a hidden one, scored on problems you never see, that decides who
actually wins.

For most of three months my agents and I worked on the public one. It was right
there. It responded to changes. It gave us a number to chase.

When the contest closed and the hidden scoreboard was revealed, I pulled my
submission history — the platform keeps the most recent fifty, which turned out
to cover the final eleven days. Of those fifty, forty-nine had been scored.

**Thirty-eight of the forty-nine scored exactly zero.** Including our best public
submission, the one we had worked toward for weeks. It was worth nothing at all.

Eleven scored something, and all eleven came from one small line of work that
tried a different kind of attack: instead of smuggling data out directly, it
talked the assistant into using its own email tool to do the sending. That line
never scored above 16.6 on the public board. On the hidden board it was the only
thing I had that scored at all.

Two things stop this from being the story it looks like.

The first is that I was not unlucky, or even unusual. Roughly two-thirds of the
four thousand teams also scored exactly zero on the hidden board. Among teams
who had done well publicly, it was about eighty percent. What happened to me was
the ordinary outcome for that contest, and most of those teams were not using AI
agents at all. It is also worth saying that only two submissions count toward
your final placing, so thirty-eight zeroes cost me nothing directly. The number
is striking. It is not, by itself, evidence of anything.

The second is the part I would rather not write.

---

## The reframe I ignored

I had assumed the email-tool line was a hunch — a portfolio instinct from years
of consulting, a bet made out of unease. That is how I told the story for months,
including in the first draft of this piece.

Then I read my own project notes.

On the first of August, three separate agents were given the contest's source
code independently and asked to work out what would survive the hidden scoring.
All three came back with the same answer: the email-tool channel, and nothing
else. The note records why, down to specific files and line numbers, including an
argument for why the hidden system would be *structurally forced* to allow that
channel — blocking legitimate email would have cost it more than it saved. The
agents then built the attack and verified it against a mock version of the hidden
scorer.

That was the first of August.

On the twenty-second of August, another note appeared in my own project memory. Its
heading, in capitals, reads: **THE REFRAME (WHY THE WHOLE SESSION OPTIMIZED THE
WRONG BOARD).** It cites the official rules page confirming that prizes are
decided solely by the hidden scoreboard, and states plainly that our
high-scoring public work was worth approximately nothing.

I flew the first email-tool submission on the twenty-third of August.

Three weeks passed between the analysis being right and my acting on it. During
those three weeks I kept spending submission slots on the public number, because
the public number gave me feedback every day and the correct answer gave me none
until the contest closed.

My own post-mortem, written before I had any idea I would be describing it
publicly, names the cause without flattering me: *sunk cost*, and *epistemic
rigor became strategic paralysis*. I had the right answer in a file. I did not
believe it enough to move.

For what it's worth, a competitor finishing fifty-first worked out the same
collapse in closed form before the reveal and bet on it properly. So it was not
only foreseeable; it was foreseen, by a human, without agents.

I finished 171st of 4,186 on the authenticated final query. I remember a
notification saying 173rd of 4,251 and a silver medal, but I did not keep it, so
treat that part as my memory rather than a record.

---

## The competition where I did better by copying

The games contest taught a different lesson, and I have to be careful how I state
it, because the last section should have taught me to distrust my own numbers.

For two months my score crawled. Then another competitor published their
notebook — their entire working solution, in public, for anyone to use. I copied
it essentially unchanged, adapted one line so it would start on my account,
submitted it with the source named, and it scored well above anything I had
managed on my own.

Copying a strong public solution is not a confession. It is ordinary practice in
these contests, and the notebook already had 149 votes, meaning everyone knew
about it. The honest question is not why I copied. It is why it took me two
months to adopt what the field had already published — a question about my
process, not about the agents.

The scale is worth stating too. Even after copying the best public solution
available, I was at roughly a third of the score of the contest leader.

---

## The ruler that wouldn't hold still

Then came the part that made me question everything before it.

I submitted an identical file twice more. It scored 3.25, then 2.58, and a third
attempt failed outright with a platform error. Unchanged code, two-thirds of a
point apart.

Then I went back and looked at where my earlier "improvements" had come from.
Almost every record I had set that summer was a resubmission of code I had
already flown. The jumps I had been proud of — a tenth of a point here, four
tenths there — were the same program, run again, landing differently. The largest
improvement I could trace to anything I actually changed was **fourteen
hundredths of a point.**

I had spent two months reading tea leaves and writing down what I saw.

This is also why I will not put a number on the copying result. The direction is
solid: everything I built in-house landed between 1.78 and 1.94, and the borrowed
notebook landed between 2.45 and 4.31, with no overlap at all. But the size of
that gap is not something this instrument can measure, and I have just finished
explaining why.

---

## Confidently wrong

The failures that worried me most were not wrong answers. They were wrong answers
delivered with complete confidence, which I caught only because I happened to
ask.

An agent adjusted a model, tested it, and reported that the adjusted version beat
the original. The numbers looked good. Something made me ask it to prove which
version had actually been running during the test.

The adjusted model had never loaded. Both sides of the comparison were the same
original model. The experiment had not produced a weak result; it had produced no
result at all, and it would have gone into my records as a success if I had not
asked an awkward question at the right moment.

That was not a one-off. An agent explained one model's poor performance as the
model being weak, when the test was set up badly enough that the other model also
scored zero under it. Another built an elaborate experiment whose branches all
changed several things at once, so no result could ever say which change
mattered.

None of these are stupid mistakes. They are the mistakes of something fluent in
the form of science without being accountable to its substance. The output looks
identical whether or not the underlying test can support it. That is the part I
find genuinely hard to work with.

I coded 38 decision points across both contests — a deliberately varied sample
chosen to span the range of outcomes, including failures, and coded by me alone,
so it is not a success rate and cannot be read as one. Eight held up. Ten held up
partly. Ten were refuted. Five turned out to be experiments that could not have
answered their own question. One was overtaken by later work, and four are still
open.

---

## What actually worked

Almost everything that saved me was a habit rather than a technology.

**Deciding the rule before seeing the number.** Late in the games contest I began
writing down, before running an experiment, exactly what result would count as
success and what would count as failure. One promising change engaged perfectly
on my own test rig — it altered the agent's behaviour exactly as designed — and
produced no improvement. Because the threshold was fixed in advance, I recorded
it as a failure and moved on. Without that rule I would have talked myself into
keeping it.

**Asking what is actually running.** After the model incident, "prove which
version is serving before we interpret anything" became a standing rule.

**Keeping the failures.** I kept a record where refuted results, invalid
experiments and unresolved ones stayed visibly different from each other.
Compressing a project into the story of what worked quietly destroys the
information you need most.

**Treating stored conclusions as claims.** Agents carry conclusions forward
between sessions, and some of them were wrong when written and grew more
confident with age. That improved my discipline, though I cannot show it changed
any result.

Two to five hours a day of this is not supervision. That is a job.

---

## What I'd tell you

**They lower the barrier, and that matters.** I did work in two unfamiliar
technical fields that would otherwise have been closed to me. If you have been
waiting for permission to try something technically ambitious, this is as good as
that permission has ever been.

**The judgment problem is not where I expected it.** I went in assuming the gap
would be that agents cannot think strategically. What I found is that mine did
the strategic thinking, correctly, and wrote it down — and that the finished
analysis sat in a file for three weeks because the wrong scoreboard was the one
giving me feedback. I should be careful here: I never actually asked an agent to
choose between the two objectives. I kept that job. So this case cannot tell you
whether agents can do strategy on demand. It can only tell you that when one
handed me the answer unprompted, I did not act on it.

**Fluency is not reliability, and they look identical.** A confident,
well-organised, clearly-written wrong answer is the failure mode you should
expect. You cannot catch it by reading the output more carefully, because the
output is not where the flaw is. You catch it by asking what was actually tested
and what was actually running.

---

## What this isn't

One person, two contests, one summer, one generation of these tools. No control
group. I chose the cases because they are mine and I coded my own records, so my
judgement is inside the results. Contest scores measure contest performance and
nothing else. I spent roughly a hundred dollars on one AI service and thirty on
another, plus subscriptions I did not track.

I did not win either contest. As I write, the games contest is still running, and
my position in it rests on a borrowed notebook and a lucky draw.

What I have is not proof of anything general. It is a detailed record of what
happened, with the failures left in — including the one I would most like to have
left out.

The lesson I came for was that AI agents cannot do the thinking. The lesson I
found is narrower and worse: on the one occasion that mattered, an agent did the
thinking, wrote it down, and I read it three weeks late.

---

*The full research paper behind this case study, with the complete evidence
record, submission-level data, and the coding of all 38 decision points, is
available as* Access Without Autonomy: An Instrumented Case Study of AI Agents
in Computational Research.
