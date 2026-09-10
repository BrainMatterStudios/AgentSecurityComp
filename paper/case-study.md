# The Feedback Trap

**Three AI agents independently worked out the winning strategy from the source
code. It still took three weeks to reach a submission. That gap, not the
analysis, is the finding.**

Over the summer of 2026 I entered two artificial-intelligence competitions in
fields I had no background in, and ran the technical work through AI coding
agents. I am not a security researcher or an AI researcher. I have spent more
than sixteen years as a consultant and architect, and most of the Python I had
written in recent years was written with assistance.

The question I wanted to answer was whether these tools genuinely lower the
barrier to technical research, or only appear to. The answer turned out to be
more interesting than either option. The agents were strong — stronger, in one
specific and uncomfortable respect, than the process I had built around them.
The constraint was not what they could work out. It was how long it took the
project to act on what they had already worked out.

---

## The two competitions

The first concerned attacks on AI assistants. Modern assistants browse, send
email, and operate other software on a user's behalf, which raises an obvious
question: can one be induced to misuse its own tools? Entrants were given a
sandboxed assistant and asked to find out. Four thousand teams took part.

The second, ARC-AGI-3, is close to the opposite problem. It gives a model a small
video game it has never seen, with no instructions, and asks it to infer the
rules by playing. People find this easy; machines do not. Nearly three thousand
teams entered.

Both fields were unfamiliar to me by design. If agents lower the barrier to
technical work, an outsider attempting exactly this is where it should show.

---

## What the agents did well

They read unfamiliar codebases quickly and turned them into something actionable.
They located the competition's own scoring code and established what it actually
rewarded, which differed from what the documentation described.

They built instruments. In the games competition an agent measured how much the
score varied between two runs of identical code — the start of a discipline that
later prevented a much more expensive mistake.

They sustained effort. Long unattended batches, careful records, no fatigue at
dead ends.

I finished just inside the top five percent of a four-thousand-team security
competition. It felt like something I could not have done alone, though with no
control group that remains an impression rather than a measurement.

---

## Two scoreboards

Competitions of this kind run two scoreboards: a public one that updates while
you compete, and a hidden one, scored on unseen problems, that determines the
result.

For most of three months the work went into the public one. It was visible, it
responded to changes, and it produced a number every day.

When the competition closed and the hidden scoreboard was revealed, I pulled the
submission history. The platform retains the most recent fifty, which covered the
final eleven days. Of those fifty, forty-nine had been scored.

**Thirty-eight of the forty-nine scored exactly zero** — including the best public
submission, the one that had absorbed weeks of optimisation.

Eleven scored. All eleven came from one comparatively small line of work using a
different mechanism: rather than moving data out directly, it induced the
assistant to use its own email tool to send it. That line never exceeded 16.6 on
the public board. On the hidden board it was the only thing that scored at all.

Before drawing any conclusion from that, two pieces of context matter.

Roughly two-thirds of the four thousand teams also scored exactly zero on the
hidden board, and among teams with strong public scores it was closer to eighty
percent. This was the ordinary outcome of that competition, and most of those
teams were not using agents. Only two submissions count toward a final placing,
so thirty-eight zeroes cost nothing directly. The number is striking; on its own
it establishes very little.

What matters is the timeline behind it.

---

## The analysis arrived early

On 1 August, three agents were given the competition's source code independently
and asked what would survive the hidden scoring. All three returned the same
answer: the email-tool channel, and nothing else.

The reasoning was specific. It cited the scoring and guardrail code by file and
line. It included a structural argument for why the hidden system would be
*obliged* to permit that channel — blocking legitimate email would have cost it
more in false positives than it gained. The agents then implemented the attack
and verified it against a mock version of the hidden scorer, on two different
models.

On 22 August a project note recorded the strategic consequence directly. Its
heading, in capitals, reads **THE REFRAME (WHY THE WHOLE SESSION OPTIMIZED THE
WRONG BOARD)**. It cites the official rules confirming that prizes are decided
solely by the hidden scoreboard, and states that the accumulated public work was
worth approximately nothing.

The first submission using that channel flew on 23 August.

So the analysis was correct, evidenced, and available three weeks before it was
acted on. The delay was not a failure of understanding. The understanding was
documented, in the repository, with citations.

---

## Why correct analysis loses to a worse metric

The mechanism is worth stating plainly, because it generalises well beyond this
competition.

The public scoreboard produced a number every day. Every experiment against it
returned a result, ranked against the field, immediately. The correct strategy
produced nothing measurable until the competition closed — by construction, since
the hidden board is hidden.

Effort follows signal. When one option supplies daily evidence of progress and a
better option supplies none until the end, attention flows to the first
regardless of expected value. The team's own project post-mortem names the
result: *sunk cost*, and *epistemic rigor became strategic paralysis*. A standard
of proof that was appropriate for a measurable question was applied to an
unmeasurable one, where it functioned as a reason to keep waiting.

This is a governance gap rather than a capability gap, and it is the failure mode
I would now design against first. The project had no mechanism for converting a
written, well-supported conclusion into a reallocation of resources. Analysis had
become cheap; the decision process around it had not changed at all.

It is worth noting that the conclusion was reachable without agents. A competitor
finishing fifty-first derived the same collapse in closed form before the reveal
and committed to it properly. The insight was available to the field; what
differed was the speed of acting on it.

The final authenticated standing was 171st of 4,186. I recall a notification
reporting 173rd of 4,251 and a silver medal, but did not retain it, so that part
is memory rather than record.

---

## The second competition: adoption, and a warning about measurement

The games competition produced a different lesson, and it needs stating carefully
in light of what follows it.

For two months the score moved slowly. Then another competitor published their
notebook — a complete working solution, public, for anyone to use. I ran it
essentially unchanged, adapting a single line so it would start on my account,
submitted it with the source credited, and it scored well above anything built
in-house.

Adopting a strong public solution is standard practice in these competitions, and
that notebook already had 149 votes, so the field knew about it. The useful
question is not why I used it, but why it took two months to adopt what had
already been published — again a question about process rather than about the
agents. Even with it, the score sat at roughly a third of the competition leader's.

Then the measurement problem surfaced. I resubmitted an identical file twice
more: it returned 3.25, then 2.58, then failed outright with a platform error.
Unchanged code, two-thirds of a point apart.

Examining every score record I had set that summer, almost all of them turned out
to be resubmissions of code already flown. The improvements I had been tracking —
a tenth of a point here, four tenths there — were the same program run again,
landing differently. **The largest improvement attributable to anything actually
changed was fourteen hundredths of a point.**

Which is also why I will not attach a figure to the adoption result. The
direction is solid: in-house work landed between 1.78 and 1.94, the public
notebook between 2.45 and 4.31, with no overlap. The size of that gap is beyond
what this instrument can resolve.

---

## Where the agents were unreliable

The failures that concerned me were not incorrect results. They were incorrect
results delivered with complete confidence, caught only because someone asked.

An agent adjusted a model, tested it, and reported that the adjusted version
outperformed the original. The figures were plausible. On being asked to
demonstrate which version had actually been running, it emerged that the adjusted
model had never loaded. Both sides of the comparison were the same model. The
experiment had not produced a weak result; it had produced no result, and would
have entered the record as a success.

There were others. One agent attributed a model's poor performance to the model,
when the test was constructed badly enough that the comparison model also scored
zero. Another built a multi-branch experiment whose branches each changed several
things at once, so no outcome could identify which change mattered.

These are not careless errors. They are characteristic of a system fluent in the
form of an experiment without being accountable to its substance, and the output
is indistinguishable either way. That property, more than any individual mistake,
is what an operating model has to account for.

Across both competitions I coded 38 decision points — a deliberately varied
sample spanning the range of outcomes, including failures, coded by me alone, so
it describes the sample rather than a success rate. Eight held up, ten held up
partly, ten were refuted, five proved to be experiments incapable of answering
their own question, one was superseded, and four remain open.

---

## An operating model

The controls that earned their place, in order of value.

**Fix the decision rule before the number arrives.** Late in the games
competition I began recording, before running an experiment, what result would
count as success and what would count as failure. One change engaged perfectly on
my own test rig, altering the agent's behaviour exactly as designed, and produced
no improvement. Because the threshold was set in advance, it was recorded as a
failure rather than argued into a success.

**Require proof of what is actually running.** After the model incident,
establishing which version was serving became a precondition for interpreting any
result.

**Measure the instrument before trusting the measurement.** Two-thirds of a point
of variation on unchanged code invalidated most of a summer's apparent progress.
That check costs one submission and should come first, not eighth.

**Keep failures distinguishable.** Refuted results, invalid experiments and
unresolved ones carry different information, and compressing a project into what
worked destroys the part you need.

**Treat stored conclusions as claims.** Agents carry conclusions between
sessions, and some were wrong when written and grew more confident with age.

**Give strong analysis a route to a decision.** This is the control this project
lacked, and the one I would add first. When an agent produces a well-supported
strategic conclusion, something has to force an explicit allocation decision
against it — a scheduled review, a standing rule that a written recommendation
gets a yes or a no rather than silence. Otherwise the option with the faster
feedback loop wins by default, which is what happened here.

Two to five hours a day went into this. That is not supervision; it is a role.

---

## What this supports, and what it does not

For anyone considering putting these tools on real work, three conclusions.

**They lower the barrier, substantially.** I did technical work in two unfamiliar
fields that would otherwise have been closed to me.

**The bottleneck may not be where you expect.** I assumed the limit would be
strategic reasoning. In this case the agents produced the correct strategic
analysis, with evidence, unprompted — and the constraint turned out to be the
decision process downstream of it. I should be precise: I never assigned an agent
the task of choosing between the two objectives, so this case cannot establish
whether they can do that on request. What it shows is that when one supplied the
answer anyway, the surrounding process was not built to use it.

**Fluency and reliability are indistinguishable in the output.** A confident,
well-organised, incorrect answer is the failure mode to design against. It cannot
be caught by reading more carefully, because the flaw is not in the writing. It
is caught by asking what was tested and what was running.

The limits are worth stating. One participant, two competitions, one summer, one
generation of these tools, no control group. I selected the cases and coded the
records, so my judgement is inside the results. Competition scores measure
competition performance. Costs were roughly a hundred dollars on one service and
thirty on another, plus untracked subscriptions. Neither competition was won, and
the games competition was still running at the time of writing.

The conclusion I expected was that AI agents cannot yet do the thinking. What the
record shows is narrower and more useful: on the one occasion that mattered most,
the thinking was done, correctly and on time, and the process around it was too
slow to convert that into a decision. Analysis is no longer the expensive part.
Acting on it still is.

---

*The full research paper behind this case study, with the complete evidence
record, submission-level data, and the coding of all 38 decision points, is
available as* Access Without Autonomy: An Instrumented Case Study of AI Agents
in Computational Research.
