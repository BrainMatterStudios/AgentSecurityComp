# The Bet I Didn't Place

**On 1 August my AI agents worked out, from the source code, the only attack
that would score. I didn't submit it until the 23rd. The three weeks in between
are the finding.**

Over the summer of 2026 I entered two AI competitions in fields I had no
background in, and ran the technical work through AI coding agents. I am not a
security researcher or an AI researcher. I have spent more than sixteen years as
a consultant and architect, and most of the Python I had written in recent years
was written with assistance.

I wanted to know whether these tools genuinely lower the barrier to technical
research. They do. What I did not expect was where the new bottleneck would
appear: not in the analysis, which arrived early and was correct, but in my own
willingness to act on it.

---

## The two competitions

The first was about attacking AI assistants. Modern assistants browse, send
email, and operate other software for you, which raises an obvious question: can
one be tricked into misusing its own tools? Entrants got a walled-off assistant
and were asked to find out. Four thousand teams took part.

The second, ARC-AGI-3, is nearly the opposite problem. It gives a model a small
video game it has never seen, with no instructions, and asks it to work out the
rules by playing. People find this easy; machines do not. Nearly three thousand
teams entered.

Competitions like these run two scoreboards. A public one updates while you
compete. A hidden one, scored under conditions you never see, decides the result.
You are allowed to submit many times, but only two submissions count toward your
final placing.

---

## What the agents did well

They read unfamiliar codebases quickly and turned them into something I could act
on. They found the competition's own scoring code and established what it
actually rewarded, which differed from the documentation.

They built instruments. In the games competition an agent measured how much the
score moved between two runs of identical code — the beginning of a discipline
that later saved me from an expensive mistake.

They sustained effort: long unattended batches, careful records, no fatigue at
dead ends.

I finished just inside the top five percent of a four-thousand-team security
competition. It felt like something I could not have done alone, though with no
control group that is an impression, not a measurement.

---

## The analysis arrived on 1 August

On 1 August, three agents were given the competition's source code in separate
sessions, with no access to each other's reasoning, and asked what would survive
the hidden scoring. All three came back with the same answer: one specific
attack, and nothing else.

The attack is worth understanding, because it is not the obvious one. Most
entrants, including me, were trying to make the assistant leak a secret. The
guardrail blocks that. The surviving attack does something subtler: it induces
the assistant to send an email it was never authorised to send. The message
carries nothing sensitive — it *cannot*, or the guardrail stops it. The
unauthorised action is itself the violation.

The agents' reasoning cited the scoring and filtering code by file and line, and
included a structural argument for why the hidden system would be *obliged* to
permit that channel: a filter aggressive enough to block ordinary email would
wrongly flag too much legitimate behaviour, and the competition's own scoring
penalised exactly that. They then built the attack and confirmed it firing on two
different models against a local replica of the public filter. No copy of the
hidden filter existed to test against — which was the whole problem.

That same note recorded two other things. First, the honest strategic position:
*"we get no private feedback before 2026-09-01, so **this is a bet, not a
tunable**."* Second, in its closing line, exactly what was stopping the
submission: *"slot economics + approval gate."*

On a one-person project, the approval gate was me.

---

## Twenty-one days, then one

For three weeks I kept spending submission slots on the public scoreboard.

It is easy to construct a structural excuse for this, and it is half true. The
public board returned a number every day, ranked against the field. The winning
attack would return nothing until the competition closed. Effort follows signal,
and I let it.

But the excuse does not survive the record, for two reasons.

The first is that I had already priced the silence. My own note said the words
"this is a bet, not a tunable" on day one. You cannot be misled by the absence of
a signal you have written down and costed. What I lacked was not information but
willingness: I would not spend a slot on a claim I could not check before the
close.

The second is that someone else did. A competitor finishing fifty-first derived
the same collapse in closed form before the reveal and committed to it properly.
They faced identical silence. My own post-mortem puts it in five words: *winners
bet under the same uncertainty.*

So what changed on 22 August? Not the evidence. A note appeared in my project
records headed **THE REFRAME** — *why the whole session optimized the wrong
board* — citing the official rules confirming that prizes are decided solely by
the hidden scoreboard, and stating that the accumulated public work was worth
approximately nothing.

The first submission using the surviving attack flew the next day.

That is the part worth taking away. The technical analysis had been correct and
available for three weeks and moved nothing. The same conclusion, rewritten as a
decision rather than a finding, converted in a day. The gap was never
understanding. It was that a correct finding and an actionable decision are
different documents, and only one of them makes anyone do something.

My own post-mortem names the cause without flattering me: *sunk cost*, and
*epistemic rigor became strategic paralysis*. I applied a standard of proof
appropriate to a measurable question to one built to withhold measurement, where
it worked as a reason to keep waiting.

The final authenticated standing was 171st of 4,186. I recall a notification
reporting 173rd of 4,251 and a silver medal, but did not keep it, so treat that
as memory rather than record.

---

## What the analysis still missed

Two things stop this being a story about agents being right and me being slow.

The agents found the surviving *channel*. Nobody computed what it was worth at
scale. My post-mortem is blunt about it: *no closed-form scorer arithmetic on the
private branch* — we tested the public board empirically instead of working out
that this attack, run at volume, was the entire private game. The channel had a
ceiling of about 60 points. The winner scored 46. My best row scored 16.8.

And the conclusion was reachable without agents at all, as the fifty-first-place
finisher demonstrated. The insight was available to the field.

---

## The second competition: copying, and a warning about measurement

For two months my score in the games competition moved slowly. Then a competitor
published their notebook — their complete working solution, in public, for anyone
to use. I copied it, adapting a single line so it would start on my account,
submitted it with the source credited, and it scored well above anything I had
built.

Copying a strong public solution is standard practice in these competitions. The
useful question is not why I did it, but why it took weeks to adopt what the
field had already published — a question about my process, not the agents. Even
with it, I sat at roughly a third of the leader's score.

Then the measurement problem surfaced. I resubmitted an identical file twice
more: 3.25, then 2.58, then an outright platform error. Unchanged code,
two-thirds of a point apart.

Looking back at every score record I had set that summer, most turned out to be
resubmissions of code already flown. The improvements I had been tracking were
the same program run again, landing differently. **The largest improvement I
could attribute to anything I actually changed was fourteen hundredths of a
point.**

Which is why I will not put a figure on the copying result. The direction is
solid — my best in-house family landed between 1.78 and 1.94, the adopted
notebook and its one-setting variant between 2.45 and 4.31, with no overlap — but
the size of that gap is beyond what this instrument can resolve. My position in
that competition still rests on a borrowed notebook and a favourable draw.

---

## Where the agents were unreliable

The failures that worried me were not wrong answers. They were wrong answers
delivered with complete confidence, caught only because I happened to ask.

An agent adjusted a model, tested it, and reported the adjusted version
outperforming the original. The figures were plausible. Asked to demonstrate
which version had actually been running, it emerged the adjusted model had never
loaded. Both sides of the comparison were the same model. The experiment had not
produced a weak result; it had produced none, and would have entered my records
as a success.

There were others. One agent blamed a model's poor performance on the model, when
the test was built badly enough that the comparison model also scored zero.
Another built an experiment whose branches each changed several things at once,
so no outcome could show which change mattered.

These are not careless errors. They are what a system fluent in the *form* of an
experiment produces when nothing holds it accountable to the substance, and the
output looks identical either way.

Across both competitions I classified 38 decision points — a deliberately varied
sample chosen to span the range of outcomes, including failures, classified by me
alone, so it describes that sample and is not a success rate. Eight held up, ten
held up partly, ten were refuted, five turned out to be experiments incapable of
answering their own question, one was superseded, and four remain open.

---

## An operating model

Six controls, with what each actually requires.

**1. Write the failure threshold before the run.** Trigger: any experiment.
Owner: whoever requests it. Artifact: one line recording what result would count
as failure, filed before execution. One change of mine engaged perfectly and
produced no improvement; because the threshold was already written, it was
recorded as a failure rather than argued into a success. Do not let the agent
propose its own threshold.

**2. Prove what actually executed.** Trigger: any comparison. Artifact: the run
must print the version identifier it loaded, and the result is void without it.
Better, make a deliberate change and confirm the output moves. This is the check
that caught the model that never loaded.

**3. Measure the instrument before trusting it.** Trigger: before the first real
comparison. Artifact: three runs of identical code, and a recorded spread. Any
difference smaller than that spread is reported as "no signal," never as
progress. This costs one run and should come first, not last.

**4. Label every result, immediately.** Trigger: on completion. Artifact: one of
five labels — held / held partly / refuted / invalid (the experiment could not
answer its own question) / open — assigned at the time and never revised
retroactively. That taxonomy is the one I used on the 38 decision points; the
"invalid" category is the one that matters, because it separates a wrong answer
from a question that was never asked.

**5. Give stored conclusions an expiry.** Trigger: session start. Agents carry
conclusions between sessions, and some were wrong when written and grew more
confident with age. Artifact: any stored conclusion must carry the evidence that
produced it and the date, or be deleted rather than inherited.

**6. Force a yes or no on written recommendations.** This is the one I lacked.
Trigger: any agent output making a strategic claim. Owner: whoever controls the
budget. Artifact: a written yes or no, dated. Silence is what cost me three
weeks, and silence is what a standing rule removes.

There is also a ninety-second diagnostic for the trap I fell into. List your
active workstreams. For each, ask when it next produces a number. **If everything
on the list produces a number this week, you are probably not working on the
thing that matters** — because the work that pays off last is the work that
competes worst for attention.

Two to five hours a day went into this. That is not supervision; it is a role,
and it needs someone senior enough to know that "prove which version was running"
is the right question.

---

## What this supports, and what it does not

**These tools lower the barrier, substantially** — though that conclusion rests
on my impression rather than a measurement, since there is no control group.

**The bottleneck may not be where you expect.** I assumed the limit would be
strategic reasoning. In this case the agents produced a correct partial analysis,
unprompted, and the constraint was my willingness to commit to it without proof
the competition was built to withhold. I should be precise: I never assigned an
agent the task of choosing between the two objectives, so this case cannot show
whether they can. What it shows is that when one produced the answer anyway, I
did not act on it for three weeks.

**Fluency and reliability look identical in the output.** A confident,
well-organised, incorrect answer is the failure mode to design against. You
cannot catch it by reading more carefully, because the flaw is not in the
writing. You catch it by asking what was tested and what was running.

The limits: one participant, two competitions, one summer, one generation of
these tools, no control group. I chose the cases and classified the records, so
my judgement is inside the results. Competition scores measure competition
performance. Costs were roughly a hundred dollars on one service and thirty on
another, plus subscriptions I did not track. Neither competition was won, and the
games competition was still running when I wrote this.

The conclusion I expected was that AI agents cannot yet do the thinking. What the
record shows is more useful and less comfortable: the thinking was largely done,
early and in writing, and it sat there because a finding is not a decision and I
was the one who had to convert it. Analysis has become cheap. Acting on it has
not.

---

*The full research paper behind this case study, with the complete evidence
record, submission-level data, and the classification of all 38 decision points,
is available as* Access Without Autonomy: An Instrumented Case Study of AI Agents
in Computational Research.
