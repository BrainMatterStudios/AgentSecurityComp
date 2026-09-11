# Access Without Autonomy: An Instrumented Case Study of AI Agents in Computational Research

## Abstract

Modern language-model agents can read a codebase, write and run code, and keep a long
investigation going for hours. This paper asks a narrower question than the usual one about
autonomy: when someone hands that machinery a real research problem in a field they do not
know, what does it actually do, and what still has to be done by a person?

The evidence is my own. Over the summer of 2026 I entered two competitions I had no background
in and ran the technical work through coding agents. One asked entrants to trick a walled-off
AI assistant into misusing its tools. The other, ARC-AGI-3, asks a model to learn an unfamiliar
video game by playing it. I kept the agents' session histories, pinned the code at fixed
revisions, saved the experiment records, and later pulled my own authenticated competition
scores. From that record I selected thirty-eight research episodes that were specific enough to
judge, and coded each one for where the idea came from, what was tested, what a human did, and
how it turned out.

The pattern is consistent across both cases. The agents were strong at getting in and getting
things running: reading unfamiliar interfaces, porting attacks onto a real code path, building
measurement tools, repairing parsers, and keeping negative results instead of burying them.
They were weak exactly where science is hard: choosing which hypothesis was worth testing,
designing experiments that could actually isolate a cause, reading their own results without
overclaiming, and producing anything genuinely original. Of the thirty-eight episodes, eight
held up, ten held up in part, ten were refuted, five turned out to be experiments that could
not answer their own question, one was superseded, and four are still open. Those labels
describe the sample I chose, not a success rate.

Neither competition was won. After the security competition closed, an authenticated query put
me 171st of 4,186. I separately saw a notification reporting 173rd of 4,251 and a silver medal,
but I did not keep it, so I treat that as memory rather than record. When the private scores
were revealed, the result was stark: of the fifty most recent submissions the platform returned,
thirty-eight scored exactly zero on the board that decided the prizes, and all eleven that scored
anything came from a single modest attack I had almost left out. Months of work on the visible
scoreboard were worth nothing on the hidden one. ARC-AGI-3 was still running as I wrote this;
its best public result came from copying a competitor's published notebook, not from anything I
built.

The honest conclusion is not that these tools cannot think. It is more uncomfortable. In the
one case where an agent produced the correct strategic analysis early and unprompted, the
analysis sat unused for three weeks, because I would not commit to a claim I could not verify
before the deadline. The bottleneck was not the agent's reasoning. It was the distance between
a correct finding and a decision someone acts on. This paper documents that gap and the working
rules I now use to close it.

## 1. Introduction

I am not a security researcher or an AI researcher. I have spent more than sixteen years in
consulting and architecture: real-time decisioning, enterprise and cloud systems, more recent
work with AI agents, and Java development early on. That background helps with systems and
structured problem solving. It does not make me an expert in agent security, in ARC-AGI-3, or in
research practice. My own coding was rusty, and most of the Python I had written recently was
written with help. So this is not a novice against an expert, and it is not a claim that general
experience substitutes for knowing a field. It is a record of what happened when an experienced
technologist entered two unfamiliar ones with real strengths and real gaps.

I set the experiment up to be demanding. Rather than feed the agents hypotheses, I withheld
domain guidance and told the first one to keep working in loops until it solved the challenge.
That licensed relentless investigation. It did not license changes to shared systems or
submissions I had not seen. My job was to approve, to challenge, to push for more breadth and
depth, and to decide when something was ready to leave my machine for a scarce scored run.

None of it was hands-off. Looking back, I spent something like two to five hours a day reading
claims, demanding better tests, redirecting work, and deciding what could proceed. I did not
track the time, so that figure is testimony, not measurement. I also believe the agents let me
take part in fields I could not otherwise have entered, and learn while doing it. That is how it
felt. It is not a measured claim about time saved, and there was no version of me working without
the tools to compare against.

Those distinctions are the whole point, and they give the paper its title. *Access* is being able
to turn a question into work that runs. *Autonomy* would need much more: choosing questions worth
asking, designing experiments that can answer them, reading the answers honestly, contributing
something original, and catching your own mistakes before someone else does. The two cases ask
which of those the agents actually had. The short answer is the first and not the rest.

## 2. Background

The word *agent* covers systems of very different scope, and the differences matter for what
follows. A conversational assistant answers one bounded prompt. A tool-using agent chases a
multi-step goal, reading files, searching, editing and running code, checking results, and
revising a plan. A closed-loop scientific system goes further still, tying its choice of what to
try next to real experiments. Throughout this paper an *AI research agent* means the middle case:
a language-model system given enough tools and persistence to do substantial parts of a
computational research workflow. The label says what the system does. It is not evidence that the
system is a scientist. The studies I cite below are peer-reviewed articles unless I call them
preprints.

Closed-loop automation is older than language-model agents. A 2004 robot scientist generated,
selected, and tested gene-function hypotheses in a yeast model, but inside a tightly bounded world
of deletion mutants and growth assays. A 2020 mobile robotic chemist ran 688 experiments in eight
days, while humans still set the study, the hypotheses, and the search space. A 2023 autonomous
materials laboratory realized 36 of 57 target compounds in 17 days, with humans choosing the
target class and the allowed ingredients, and manual follow-up where measurements were
inconclusive. These systems are genuinely autonomous inside an engineered envelope. That is not
general scientific autonomy, and their constraints are unlike a coding agent's: a laboratory couples
a fixed goal to instruments and feedback, while a language-model agent roams between literature,
code, conjecture, and prose with no reliable way to tell whether the resulting chain holds
together.

The work on language-model agents now spans the whole workflow, and the task boundaries matter as
much as the headlines. Given materials-science problems, GPT-4 produced hypotheses along with a
high error rate and a need for expert review: a demonstration, not a discovery. ScienceAgentBench
turned 102 tasks from real papers into checkable programming problems, and baseline agents solved
only a minority even with repeated attempts and hints. A 2026 study of a biomedical "co-scientist"
reported hypotheses with early laboratory validation, with experts in the loop throughout and the
evidence concentrated in one field. The broader claims come from preprints, and they are candid
about their limits: one data-to-paper pipeline produced simple manuscripts on autopilot while
reporting thin novelty and a rising need for human help as complexity grew; an end-to-end "AI
scientist" reported implementation failures, weak rigor, and occasional invented results. The
benchmarks tell the same story. On discovery and reproduction tasks, the best agents top out around
a fifth to a quarter of what the task demands, and reproducing existing work is far easier than
doing new work. Reviewers rated machine-generated research ideas as slightly more novel but less
feasible than human ones, though nobody executed the ideas and the system could not reliably rank
its own output. Even the clerical parts need checking: a 2023 study found fabricated citations, and
errors inside real ones, in generated literature reviews.

Read together, this literature supports a map of separate capabilities, not a single autonomy
score. Agents can do useful pieces of research, and can sometimes chain many pieces into a long
workflow. They also degrade with complexity, with hidden evaluation, with broken controls, with
unreliable self-assessment, and with weak provenance. This paper treats them as research
executors whose output earns trust one episode at a time, and it refuses to read autonomy off
fluency, tool use, token counts, or a finished-looking manuscript.

## 3. Method

This is a comparative single-participant study, an N-of-1 design, of one researcher using several
coding agents across two projects. The security competition is the primary case; ARC-AGI-3 is the
comparison. The two are not a controlled experiment. They surface recurring activities and failure
modes in different settings, but they were not matched or randomly assigned, so nothing here
measures one provider against another or estimates how much faster the work went.

The evidence has five kinds. Private session histories from Claude Code, Codex, and
OpenCode/DeepSeek record what the agents proposed and did. Pinned repository revisions and saved
artifacts fix the code and results at known points in time. Experiment logs record what was run.
Authenticated competition queries supply the scores. And a set of my own interview answers supplies
the parts only I can report, such as the daily oversight estimate; those are labelled as testimony
throughout. Literature and policy sources supply context and prove nothing about either project.
Four companion documents carry the full evidence: a private ledger keyed by source, a redacted
public ledger that reproduces all thirty-eight episodes with public locators so a reviewer can
check the tallies, a manifest recording what survived a later audit, and two dated live-results
files holding the post-competition queries. An audit on 4 September found three of the ten
canonical Claude files missing from their recorded paths; claims that rested on them fall back to
repository corroboration or an explicit testimony label.

The unit of analysis is a *research episode*: a bounded piece of work carrying one claim specific
enough to judge, with traceable evidence, an implementation or experiment, and a lesson. Routine
debugging and repeated variants that raised no new question were left out. This is a chosen sample
built for variety, not a census, so the counts describe these episodes and nothing wider. Each
episode is coded for where its claim appears to originate (human, agent, external, or a mix), what
evidence preceded it, what a human did, how it turned out locally, how it turned out on a scored
run, and its final status. The six statuses do real work and are worth stating plainly:

| Status | What it means |
| --- | --- |
| Confirmed | The claim held up under a test that could have refuted it. |
| Partially supported | Part of the claim held; part did not, or held only in a bounded form. |
| Refuted | A valid test contradicted the claim. |
| Invalid experiment | The test could not answer its own question, because a control was broken or the treatment never ran. This is not a negative result; it is a non-result. |
| Superseded | Later work displaced the claim before it was cleanly settled. |
| Open | Not yet resolved by the available evidence. |

Caption: The six episode statuses. The "invalid experiment" label is the one that matters most, because it separates a wrong answer from a question that was never actually asked.

Two rules keep the coding honest. Local outcomes and scored outcomes stay in separate fields, so a
working implementation is never mistaken for an effect that transferred to the real evaluation. And
the record is kept as a living document: repository claims name a pinned revision, later
observations are appended as new dated states rather than overwriting old ones, and a negative,
superseded, or unresolved result is never quietly rewritten into a success. The security
competition closed on 1 September; ARC-AGI-3 was still open when I wrote this, so its numbers are a
mid-competition snapshot, not a result. A short glossary of the competition-specific terms used
below appears once, here, so the case narratives can stay in plain language.

| Term | Meaning in this paper |
| --- | --- |
| Public board | The scoreboard that updates during the competition. A development signal only. |
| Private board | The hidden scoreboard, scored under conditions you never see, that decides the prizes. |
| Submission slot | A scored run. They are rationed; only a fixed number count toward the final placing. |
| Exfiltration | An attack that makes the assistant send a protected secret out through a tool call. |
| Confused deputy | An attack that makes the assistant take an action it was not authorised to take, carrying nothing sensitive. The action itself is the violation. |
| Ladder | A set of related scored runs that vary one thing at a time. |
| Arm and control | One variant being tested, measured against an unchanged baseline. |
| Draw | One run of an unchanged submission. Repeated draws of the same code can score differently. |

Caption: The competition vocabulary, defined once. The public-versus-private board distinction is the hinge of the whole security case.

## 4. Primary case: the AI agent security competition

The competition gave entrants a walled-off AI assistant that could browse, send email, and operate
other tools, and asked a simple question: could it be tricked into misusing those tools? Around
four thousand teams took part. Every submission was scored twice, on a permissive public guardrail
you could see and a stricter private guardrail you could not, and the prizes were decided by the
private board alone. That last fact is the pivot of everything that follows, and I did not
internalise it until very late.

The work opened in mid-June with the broad instruction to keep iterating toward the goal. The agent
worked first against a mock scaffold, then read the real competition SDK and ported the attack onto
its actual interface. It also raised the number of candidate attacks, having read the scorer as
additive. The real code path ran and carried every later submission; the extra volume set a
baseline and solved nothing. Both were competent acts of inspection, and neither shows the system
picking an important direction on its own.[^entry] Two weeks later the contract changed under us:
fabricated secret-like strings stopped scoring, because a new SDK version wanted a genuine sentinel
value read from the protected file. The agent adopted the real marker, checked it locally, and
scoring resumed. This is why plumbing can be research: a plausible attack was worth nothing until it
obeyed the evaluator's protocol.[^marker]

Then came a stretch of borrowing and measurement. In late July the agent reproduced, in bounded
form, a public technique that sized its output to the time available in the scored environment, so a
submission would not time out. It ran cleanly in local replay. A later check found every one of
those scored rows had come back with an error status, so the visible score differences established
nothing about a completed run.[^sizing] The same pattern repeated for two throughput ideas, cutting
off decoding early and packing several messages into one call: both moved the local timing and both
only ever reached errored rows.[^throughput] This is the reason I keep local and scored outcomes in
separate fields. The code worked. Whether it helped a real run stayed unknown.

### The analysis that arrived early

On 1 August I ran an unusual check. I gave the competition source code to three agents in separate,
firewalled sessions, each with no access to the others or to my own notes, and asked what would
survive the hidden scoring. All three came back with the same answer: one specific attack, and
nothing else. The attack was not the obvious one. Most entrants, including me, were trying to make
the assistant leak the secret, and the public filter has a hole that lets that score. The surviving
attack instead induces the assistant to send an unauthorised email whose body carries nothing
sensitive. It cannot carry anything sensitive, or the guardrail stops it; the unauthorised action is
itself the violation. The agents cited the scoring and filtering code by line, and added a
structural argument for why a stricter hidden filter would be *obliged* to allow that channel: a
filter aggressive enough to block a benign email would wrongly flag ordinary, legitimate email, and
the competition's own scoring penalised exactly that kind of false alarm.[^triangulation]

Two things in that same note matter as much as the finding. It priced its own uncertainty in
writing: we would get no private feedback before the deadline, so *this is a bet, not a tunable*.
And it named, in its closing words, exactly what stood between the analysis and a submission: *slot
economics and an approval gate*. On a one-person project, the approval gate was me.

The agent built the attack that day. What it built did not yet work. Its first real scored test, two
days later, came back void: the benign-email framing ran the model through too many steps and blew
the timing budget the sizing logic depended on. The channel was right; the implementation was not,
and it needed a terminating template and a more conservative size before it would score at all. This
is worth stating plainly, because the temptation is to remember the 1 August analysis as a finished
weapon left in a drawer. It was a correct direction with a broken first build. What it was missing
after the repair was not more engineering. It was a decision to treat it as the primary bet rather
than a hedge.

### Three weeks on the wrong board

For most of August I kept spending scored runs on the public board. Some of that has a structural
excuse, and the excuse is half true: the public board returned a number every day, ranked against
the field, while the surviving attack would return nothing until the competition closed. Effort
follows signal. But the excuse does not survive the record, because I had already priced the
silence in my own words on day one. You cannot be misled by the absence of a signal you have written
down and costed. What I lacked was not information but willingness to commit a scarce run to a claim
I could not check before the deadline.

The public-board work of those weeks was real engineering and, on the board that decided the prizes,
worth nothing. Some of it produced clean negatives that are worth keeping. An early model comparison
read one model as weak, but the comparison ran on an underpowered message frame that also drove the
supposedly strong model to zero; with a broken control it proved nothing either way.[^gemma] A later
routing experiment moved several factors at once, so its differing scores could never point to any
one cause.[^router] A borrowed "commitment forge" technique, which pushes a reasoning model to make
several tool calls inside one candidate, reproduced its component behaviour but never reached its
stated target when recombined with board-routing and model variants.[^forge] A run of late ladders in
mid-August, testing probe counts, a GPU path, and multi-message packing, all came back below the
historical baseline and without matched controls, so each refuted a narrow threshold claim without
establishing anything causal.[^ladders] The one governance move that paid off here cost nothing and
scored nothing: I told a fresh agent to distrust the stored memory and revalidate everything, which
turned inherited conclusions back into claims to check rather than facts to build on.[^memblind]

What changed on 22 August was not the evidence. A note appeared in my records headed *the reframe*,
citing the official rules I had finally read closely: the prizes are determined solely by the
private board, and the public number I had chased all month was explicitly not a guarantee of
anything on the board that paid. The accumulated public work was, for prize purposes, worth
approximately nothing. The repaired confused-deputy hedge first flew as a scored submission two days
later. The technical analysis had been correct and available for three weeks and moved nothing. The
same conclusion, rewritten as a decision rather than a finding, converted in a day. The gap was
never understanding. A correct finding and an actionable decision are different documents, and only
one of them makes anyone do something.

### What the private board actually paid for

The competition closed on 1 September. My authenticated final standing was 171st of 4,186. I recall
a notification reporting 173rd of 4,251 and a silver medal, but I did not keep it, so I treat that as
memory, not record.[^standing]

When I queried my own private scores, the dissociation was almost total. The platform returns the
most recent fifty submissions; mine span the final eleven days. One errored; forty-nine carried both
scores. Thirty-eight of those scored exactly zero on the private board. The eleven that scored
anything all came from the confused-deputy email line, between 2.29 and 16.81. Nothing above fifty
points of public score earned a single private point, including the 92.67 public row I had selected
as one of my two final entries. My two selections tell the story on their own: one was the banked
public best, at 92.67 public and 0.00 private; the other was the confused-deputy hedge, at 16.56
public and 16.74 private. The board I had optimised for months paid nothing. The small hedge I had
almost not committed to was the entire result.[^reveal] This is a complete account of the
submissions I actually flew, which is a stronger claim than a sample, and it is still only a claim
about one entrant's last eleven days. It does not reveal what the hidden guardrail was, why those
rows scored, or whether the hedge is what produced the final rank.

Two honest limits close the case. First, the analysis found the surviving *channel* but never
computed what it was worth at scale; I tested the public board empirically instead of working out
that this attack, run at volume, was the whole private game. Second, the conclusion was reachable
without agents at all. In a final-week attempt to close the visible gap, every attacker-controllable
lever I tried failed to beat my own best public row while a direct query showed the frontier had
already reached at least 147.5, roughly 1.6 times my best; exhausting that family of levers is a
valid negative result, not proof the gap was unclosable.[^frontier]

## 5. Comparative case: ARC-AGI-3

ARC-AGI-3 is almost the opposite problem. It hands a model a small video game it has never seen,
with no instructions, and asks it to work out the rules by playing. People find this easy; machines
do not. The state, the goals, and the evaluator's lifecycle were only partly visible, which made it a
different test of the same agents: exploration had room to run, but every idea still had to clear a
human challenge, a local test, and a scarce scored run.

Several early episodes show the recurring shape of the failures. A proposed reset trick between
plays produced a large local effect, then returned an error in competition mode, which made the test
invalid for the very setting it claimed to help.[^reset] A search-and-replay solver, exploiting the
fact that scoring kept the best run, solved all twenty-five development games; the solver was real
and the scoring trick did not survive external conditions, so the conclusion split cleanly in
two.[^replay] The sharpest failure came in mid-July. A fine-tuned adapter appeared to beat its base
model, and the agent was confident, until I asked for proof of which model was actually running. The
adapter had never loaded. Both sides of the comparison were the same model. This was not a failed
experiment; it was no experiment, and it would have entered my records as a success.[^lora] A prompt
change the following day is the instructive contrast: it genuinely ran, raised the development score,
and then simply did not carry over to the hidden evaluation. That is a refuted transfer claim, and it
is what a valid negative looks like next to a non-result.[^prompt]

The clearest value in this case, as in the other, came from measurement and infrastructure rather
than from any winning idea. On 1 August the agent measured the evaluator's own noise by running the
same code against itself several times, and found a spread of about 0.7 game levels between identical
runs. That single number turned two planned comparisons into ones I could see were underpowered, and
the protocol was amended before any small difference was read as signal.[^noise] Perception work made
this concrete: reworking how the game state was presented to the reasoner moved a retained comparison
from zero out of nine to six out of six, though two things changed at once, so nothing isolates which
one did the work.[^perception] Structural planning, best-of-N selection, and a repaired memory
strategy were all built and all stayed inside their established score bands.[^structural] A broad
multi-agent literature search turned out to have drawn its corpus from the wrong model, which made
its breadth worthless.[^corpus] Out of these failures the agents and I built a reusable gate, "serving
identity proven first," that made proving which model was running a precondition for any claim rather
than a cleanup after a surprising score.[^gate]

By the original cutoff, later engineered candidates had failed to replace the reference policy, and a
promising external model remained untested on the hidden board, so it stayed open.[^late] The winning
objective was unmet. None of that erases the search, perception, and calibration work, which was
genuine; it sets the outer boundary of the case.

### A better rank on someone else's notebook

ARC-AGI-3 was still running as I wrote this, and its numbers kept moving, so what follows is a dated
snapshot, not a result. Over early September my public rank rose from 374th to 26th, and my best
public score from 1.94 to 4.31, against a leader on 11.04. Taken alone that is the most encouraging
number in the whole study. How it happened matters more than the rank.

The jump came from copying a competitor. On 5 September I submitted a byte-for-byte copy of a public
notebook, credited in the submission itself, and it scored 3.25 against my best in-house result of
1.94. Copying a strong public solution is standard practice in these competitions, so the useful
question is not why I did it but why it took weeks to adopt what the field had already published.
The comparison cuts deeper than the single step. Most of my earlier record-setting moves had changed
no code at all; they were the same program resubmitted and landing differently. The largest
improvement I can trace to anything I actually changed was fourteen hundredths of a point.[^copy]

The reason I will not put a firmer figure on the copying result is that the metric barely holds
still. I submitted one identical file three times and got 3.25, then 2.58, then an outright platform
error. The one adjusted candidate returned 4.31 on one draw and 2.45 on another. Unchanged code spans
two-thirds of a point; the candidate spans nearly two. My rank rests on the best draw of that spread,
and nothing in the public record separates it from noise.[^draws]

That instability had a practical consequence, and it is the one place in this study where the working
rules below were applied *before* a result rather than derived from a failure after it. With draws
that wide and slots that scarce, the public board could not settle a one-setting question, so I tested
the levers off the platform instead, on my own rig, with the decision rules written down before each
run. Two candidates went through it. One changed the agent's behaviour substantially and moved the
score not at all. The other engaged every mechanism it was designed to engage and landed squarely
inside the band I had declared dead before launch, so it was recorded dead.[^rig] Neither is live
evidence: a null on my own rig no more refutes a real competition effect than a gain on it would
establish one. The live confirmation was still unfinished at the cutoff and is recorded as open.

Neither headline moved. The security prize was not won and the standing did not change; ARC-AGI-3's
objective was unmet and its private board stays closed until its own deadline. What the second case
adds to the first is a cleaner view of the same boundary: the largest gains came from copying and
from luck in a noisy metric, and the two ideas my agents originated and I tested against pre-declared
rules both came back null.

## 6. Findings

The plainest way to state the result is that "agentic research" bundles six different things that
should be judged separately. *Access* is getting into an unfamiliar domain and starting useful work.
*Execution* is turning a proposed mechanism into code, instruments, and experiments. *Insight* is an
explanation the evidence supports over its rivals. *Originality* is where the question or method came
from. *Reliability* is producing valid, well-calibrated results episode after episode. *Autonomy*
would mean holding all five together dependably, and stopping or correcting yourself before a human
catches the critical mistake. Across both cases the agents showed access clearly, execution
substantially, insight in places, and not much dependable originality, reliability, or autonomy. Of
the thirty-eight coded episodes, none originated with me alone, sixteen with an agent, four with an
external source, and eighteen from a mix; but an agent-origin idea was not therefore original, since
it could recombine a known method, chase an already-visible failure, or end up refuted.[^origins]

Where the agents added value, the value was spread across the workflow rather than concentrated in
discovery, and it survived even when the claim that motivated it failed.

- **Getting in and getting oriented.** Searching repositories, reading unfamiliar SDKs, and working
  through evaluators turned opaque systems into something I could act on. This is what my sense of
  access rests on, and it is testimony, not a measured comparison against working unaided.
- **Building things that run.** Attack candidates, a search-and-replay solver, serving probes, parsers,
  routers, replay-safe sizing, gated runners. These artifacts kept their value after the score claim
  behind them was refuted or never adjudicated.
- **Making hidden assumptions measurable.** Timing probes, a router's self-measurement, serving-identity
  checks, and the evaluator-noise estimate. The noise number and the "serving identity proven first"
  rule are stronger contributions to research validity than any leaderboard narrative.
- **Reusing public methods with their provenance intact.** The adaptive-sizing and commitment-forge
  work came from outside; the agents brought it in, tested it, and combined it. That is implementation
  and adaptation, not invention, and keeping the distinction visible is the honest way to report it.

Where they struggled, the failures were rarely wrong answers delivered as wrong answers. They were
confident, well-organised answers that happened to be built on a broken foundation, and I caught them
mostly because I asked, not because they read as doubtful. Hypothesis selection and novelty stayed
weak: I could not point to a single unexpected discovery the agents originated, and the sharpest
evidence for this arrived late, when the largest gain in the second case came from copying a notebook
and the two ideas we did originate and test against fixed rules both returned null. Calibration failed
where it mattered most, with high confidence sitting right before the discovery that a treatment never
served, that a control was underpowered, or that a corpus was for the wrong model. Causal reasoning
broke whenever the arms of an experiment moved more than one thing at once. And the line between a
local result and a scored one gave way repeatedly: code that worked, or moved a number inside the
harness, could not show that a thing was deployed, that it generalised, or that it won. Knowing when to
stop, and what to forget, did not come from the agent on its own; a stored summary would carry last
week's assumption into this week's run with more confidence than when it was written.

Underneath all of this sits the human loop. My two-to-five hours a day of reading, challenging,
redirecting, and approving was not a backstop bolted onto an autonomous system. It was part of the
machine. That intervention is what exposed the broken controls, forced proof of which model was
serving, kept unresolved arms pending, and stopped an unserved idea from spending a scarce run. This
is supervised execution at scale. It is not hands-off autonomy, and nothing in the record suggests it
was close.

## 7. Working rules

The rules below are a research protocol, not general advice to keep a human in the loop. Each one
answers a specific failure in the record, and each names an artifact you can check for. Most were
learned in hindsight; the one prospective application, on the off-platform rig in the second case, is
why I trust them.

1. **Write the failure threshold before the run.** For any experiment, record in one line what result
   would count as failure, filed before execution, and do not let the agent set its own threshold. One
   change of mine engaged perfectly and produced no improvement; because the line was already written,
   it was recorded as a failure instead of argued into a success.
2. **Prove what actually executed.** For any comparison, make the run print the version it loaded, and
   treat the result as void without it. This is the check that caught the adapter that never served.
3. **Measure the instrument before you trust it.** Before the first real comparison, run identical code
   several times and record the spread. Any difference smaller than that spread is "no signal," never
   progress. It costs one run and belongs first, not last.
4. **Label every result immediately.** Assign one of the six statuses at the time, and never revise it
   retroactively. The "invalid experiment" label is the one that earns its keep, because it stops a
   broken test from being filed as a negative result.
5. **Give stored conclusions an expiry.** Agents carry conclusions between sessions, and some were wrong
   when written and grew more confident with age. A stored conclusion must carry the evidence and date
   that produced it, or be deleted rather than inherited.
6. **Force a yes or no on written recommendations.** This is the rule I most lacked. Any agent output
   making a strategic claim needs a dated, written decision from whoever controls the budget. Silence
   cost me three weeks, and a standing rule is what removes silence.
7. **Resolve every decisive input to its primary source.** Pin the version and access date, and verify
   the quoted claim before it enters a hypothesis. A guardrail's name is not its behaviour; a
   citation-shaped string is not provenance.
8. **Gate scarce runs and shared state behind named human approval.** Before any scored run, external
   submission, or write to a shared system, a person checks the threshold, the control, and the stop
   rule. This is what kept an unserved idea from burning a slot.
9. **Preserve negatives, killed arms, and pending states.** Append results to an immutable ledger with
   separate local and scored fields. A success-only narrative erases exactly the distinctions that make
   the record trustworthy.

There is also a ninety-second diagnostic for the trap I fell into. List your active workstreams, and
for each, ask when it next produces a number. If everything on the list produces a number this week,
you are probably not working on the thing that matters, because the work that pays off last competes
worst for attention. The division of labour follows from all of this: agents can fill in the thresholds,
build the controls, keep the ledger, and run first-pass audits, but the accountable person decides
whether the design identifies the claim, whether a scarce run is worth spending, and what the evidence
actually supports. That role needs someone senior enough to know that "prove which version was running"
is the right question to ask.

## 8. Limitations

This is one researcher and two projects, chosen because I ran them, with thirty-eight episodes I both
selected and coded. No second coder worked blind, so there is no inter-rater reliability figure, and my
judgement is inside the results. A reviewer can audit the public locators in the redacted ledger but
cannot re-derive the coding from the private histories, three of which were missing at the later audit.
There was no human-only control, no matched budget, and no stable model baseline, so nothing here is a
productivity estimate or a provider ranking; the providers were used unequally and for different
purposes, and their models changed during the window. Competition scores are imperfect proxies for
research quality, and hidden evaluators, run-to-run variance, scarce slots, and incomplete local
replicas all limit how far a local result can speak to a scored one. Several load-bearing statements are
testimony rather than measurement: my baseline, the daily oversight hours, the perceived value, the
costs, and the unwon objectives. Costs were roughly a hundred dollars on one service and thirty on
another, plus subscriptions I did not track. The security case is settled; the ARC-AGI-3 numbers are a
mid-competition snapshot resting on the best draw of a noisy metric, and will have moved since.

## 9. Living record

The record is kept so that later observations extend it rather than overwrite it. The original cutoff
was 16 August; two later dated cutoffs, on 4 and 8 September, appended the competition's close and a
mid-competition ARC snapshot without touching the earlier narrative. The rule is strict: a pending
result stays pending and an unqueried one stays unqueried until direct evidence changes it, and a new
result never silently replaces a negative or unresolved one. At the latest cutoff the security standing
was 171st of 4,186 with the private-board dissociation described above; ARC-AGI-3 was 26th of 2,892 on a
best public score of 4.31 against an 11.04 frontier, with its private board unrevealed until its
November deadline. The reported silver medal, the receipt-reconciled costs, the measured oversight, and
the working-note award outcome remain reserved fields, to be filled only from a cited record or an
explicit testimony label. The full dated states and the per-claim retrieval limits live in the two
live-results artifacts and the appendix.

## Declarations

**Data and materials.** The redacted public episode ledger provides all thirty-eight coding rows with
their origins, statuses, and public locators, and the two live-results artifacts hold the
post-competition queries and their per-claim limits. The private Claude, Codex, and OpenCode histories
are controlled because they can contain credentials and unrelated material; their file digests are
recorded in the source manifest, and an authorized audit can inspect the surviving originals under the
quotation and redaction rules in the appendix. Three canonical Claude files were absent at the 4
September audit.

**Ethics and reflexivity.** This is a retrospective self-study of my own agent interactions and project
artifacts. It recruited no external participants and publishes no private third-party conversation
content. I am at once the participant, the analyst, and the sole coder, which creates unavoidable risks
of recall, selection, and interpretation bias; the public ledger, the testimony labels, the
missing-source disclosures, and the narrow claim statuses are meant to make those risks inspectable, not
to eliminate them.

**Funding and interests.** No external research funding supported this study. Direct service costs are
reported only as testimony because receipts were not reconciled by case. I operate BrainMatterStudios
and used commercial AI and compute services, and I declare no provider sponsorship of the study or this
manuscript.

**Correspondence.** Ahmed Mobasher, BrainMatterStudios, The Hague, Netherlands, and Cairo, Egypt,
reachable through brainmatterstudios.com. Keywords: AI research agents; computational research;
scientific autonomy; human oversight; research integrity; N-of-1 study.

## Acknowledgements and AI-Use Disclosure

I am the sole author and am accountable for every claim, citation, and word in this paper. Claude Code
was the primary agent used to run the research across both cases. Codex and OpenCode/DeepSeek were used
as supplementary perspective resets and challenge mechanisms, and their unequal use supports no provider
ranking. In preparing this manuscript, an agent assisted with evidence-ledger review, source
reconciliation, drafting, and mechanical checks; all such material was treated as provisional and
checked against the evidence ledger. Editorial guidance from the ICMJE and Springer Nature bars AI tools
from authorship and keeps accountability with the human, and I follow it here: none of Claude Code,
Codex, OpenCode, or DeepSeek is an author.

## References

1. King, R. D., Whelan, K. E., Jones, F. M., et al. "Functional genomic hypothesis generation and
   experimentation by a robot scientist." *Nature* 427, 247–252 (2004).
   [doi:10.1038/nature02236](https://doi.org/10.1038/nature02236).
2. Burger, B., Maffettone, P. M., Gusev, V. V., et al. "A mobile robotic chemist." *Nature* 583,
   237–241 (2020). [doi:10.1038/s41586-020-2442-2](https://doi.org/10.1038/s41586-020-2442-2).
3. Szymanski, N. J., Rendy, B., Fei, Y., et al. "An autonomous laboratory for the accelerated synthesis
   of inorganic materials." *Nature* 624, 86–91 (2023).
   [doi:10.1038/s41586-023-06734-w](https://doi.org/10.1038/s41586-023-06734-w).
4. Park, Y. J., Kaplan, D., Ren, Z., et al. "Can ChatGPT be used to generate scientific hypotheses?"
   *Journal of Materiomics* 10(3), 578–584 (2024).
   [doi:10.1016/j.jmat.2023.08.007](https://doi.org/10.1016/j.jmat.2023.08.007).
5. Chen, Z., Chen, S., Ning, Y., et al. "ScienceAgentBench: Toward Rigorous Assessment of Language
   Agents for Data-Driven Scientific Discovery." ICLR 2025.
   [OpenReview 6z4YKr0GK6](https://openreview.net/forum?id=6z4YKr0GK6).
6. Gottweis, J., Weng, W.-H., Daryin, A., et al. "Accelerating scientific discovery with Co-Scientist."
   *Nature* 655, 487–496 (2026).
   [doi:10.1038/s41586-026-10644-y](https://doi.org/10.1038/s41586-026-10644-y).
7. Ifargan, T., Hafner, L., Kern, M., Alcalay, O., and Kishony, R. "Autonomous LLM-driven research from
   data to human-verifiable research papers." arXiv 2404.17605v1 (2024).
   [arXiv:2404.17605](https://arxiv.org/abs/2404.17605).
8. Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., and Ha, D. "The AI Scientist: Towards Fully
   Automated Open-Ended Scientific Discovery." arXiv 2408.06292v3 (2024).
   [arXiv:2408.06292](https://arxiv.org/abs/2408.06292).
9. Majumder, B. P., Surana, H., Agarwal, D., et al. "DiscoveryBench: Towards Data-Driven Discovery with
   Large Language Models." arXiv 2407.01725v1 (2024). [arXiv:2407.01725](https://arxiv.org/abs/2407.01725).
10. Siegel, Z. S., Kapoor, S., Nadgir, N., Stroebl, B., and Narayanan, A. "CORE-Bench: Fostering the
    Credibility of Published Research Through a Computational Reproducibility Agent Benchmark." arXiv
    2409.11363v2 (2024; revised 2026). [arXiv:2409.11363](https://arxiv.org/abs/2409.11363).
11. Starace, G., Jaffe, O., Sherburn, D., et al. "PaperBench: Evaluating AI's Ability to Replicate AI
    Research." arXiv 2504.01848 (2025). [arXiv:2504.01848](https://arxiv.org/abs/2504.01848).
12. Si, C., Yang, D., and Hashimoto, T. "Can LLMs Generate Novel Research Ideas? A Large-Scale Human
    Study with 100+ NLP Researchers." arXiv 2409.04109v1 (2024).
    [arXiv:2409.04109](https://arxiv.org/abs/2409.04109).
13. Skarlinski, M. D., Cox, S., Laurent, J. M., et al. "Language agents achieve superhuman synthesis of
    scientific knowledge." arXiv 2409.13740v2 (2024). [arXiv:2409.13740](https://arxiv.org/abs/2409.13740).
14. D'Arcy, M., Hope, T., Birnbaum, L., and Downey, D. "MARG: Multi-Agent Review Generation for
    Scientific Papers." arXiv 2401.04259v1 (2024). [arXiv:2401.04259](https://arxiv.org/abs/2401.04259).
15. Walters, W. H., and Wilder, E. I. "Fabrication and errors in the bibliographic citations generated by
    ChatGPT." *Scientific Reports* 13, 14045 (2023).
    [doi:10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5).
16. International Committee of Medical Journal Editors. "Use of AI by Authors." Checked 2026-08-16.
    [ICMJE guidance](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html).
17. Springer Nature. "AI guidance for researchers and communities." Checked 2026-08-16.
    [Springer Nature guidance](https://group.springernature.com/gp/group/ai/ai-guidance-for-our-researchers-and-communities).

## Appendix A: Methods and Evidence

**Sources and cutoffs.** Each revision fixes separate cutoffs for repositories, mutable agent stores,
live queries, and audit-time artifacts. Repository claims name a pinned revision; a later extraction of
a mutable store is treated as a new observation, not a re-reading of the old one. The security repository
is pinned at one commit and the ARC repository at another, with the agent stores extracted at a recorded
time under recorded filters.

**Episodes and coding.** An episode is a bounded, adjudicable claim with traceable evidence, an
implementation or experiment or explicit adjudication, and enough record to code origin and status.
Sampling was purposive and sought variation across cases, mechanisms, outcomes, validity failures, and
governance lessons; it was not a census, and no all-events denominator exists. Origin is coded
conservatively: an idea is coded to an agent only when no material human or external input shaped it,
public-method reproduction is external, and substantial combinations are mixed. Status belongs to the
claim, not to the artifact, so a working implementation can coexist with a refuted efficacy claim, and a
broken control yields an invalid experiment rather than a negative result. Because one person coded the
sample, a later recode must keep the old row, state the changed field and reason, and recompute the
totals rather than rewrite history.

**Evidence authority.** Three tiers are kept distinct. A direct record is a primary publication, pinned
code or artifact, exact local measurement, or identified scored row. A triangulated finding rests on at
least two independent direct records. Inference, testimony, and open hypotheses form the third tier. A
local measurement and a scored observation answer different questions, and neither automatically outranks
the other; a claim is promoted only to the scope its source, control, and evaluator establish.

**Quotation and privacy.** Only short, authorized excerpts about hypothesis formation, confidence,
correction, intervention, or governance are eligible, each traceable in the private record to case,
provider, session, timestamp, speaker, and context. Secrets, credentials, unrelated personal material,
and meaning-altering truncation are excluded; where safe redaction would change meaning, the passage is
paraphrased or omitted.

**Cost, oversight, and updates.** Costs are recorded by date, vendor, currency, amount, and case
allocation, and only receipt-supported amounts may enter a confirmed total; the figures here are
testimony, and human time is reported separately from cash. Each post-competition update freezes the
prior state, adds a dated cutoff, retrieves official results and identifiers, appends every newly
completed, failed, cancelled, or pending run without inferring an unrun result from a companion, recodes
an episode only when new evidence changes its bounded claim, and rechecks the venue's current
authorship and disclosure rules before submission.

## Notes

These notes carry the evidence for the narrative claims above, keyed to the coded episodes in the public
ledger and to the dated live-results artifacts. Episode identifiers beginning `AS` belong to the security
case, `ARC` to ARC-AGI-3, and `OC` to the supplementary OpenCode investigations; quote identifiers
beginning `Q` are the authorized excerpts in the quote ledger.

[^entry]: Episodes AS-S01–AS-S02; quote Q01. Real-path port and candidate scaling, mid-June; the volume set a baseline and did not select a direction.
[^marker]: Episode AS-S03. The SDK 3.1.2 sentinel-marker repair; a plausible attack scored nothing until it matched the evaluator's protocol.
[^sizing]: Episode AS-S04. Adaptive sizing reproduced from a public method; the five identified scored rows all carried an `ERROR` status, so the visible score difference is not a completed effect.
[^throughput]: Episodes AS-S05–AS-S06. Early-close and message-packing throughput work; every identified scored row was `ERROR`, and efficacy stayed unadjudicated.
[^triangulation]: The three firewalled sessions and the confused-deputy channel are documented in the private-hedge session record and the 1 August commit that built the channel (`JED_RS_CHANNEL=deputy`), with the false-alarm argument grounded in the scoring code; the "bet, not a tunable" and "slot economics and approval gate" phrasings are from that record. The first scored test voided on 3 August and the channel was repaired before it scored. The pivot and final selection are coded as episode AS-S15 (origin mixed). Repository- and testimony-corroborated.
[^gemma]: Episode AS-S07. The model comparison ran on an underpowered frame that also drove the other model to zero; invalid experiment.
[^router]: Episode AS-S08. The routing ladder moved several factors at once, so no arm could isolate routing; invalid experiment.
[^forge]: Episodes AS-S09–AS-S10. Reproduction of the public commitment-forge method and its recombination; component behaviour partially supported, stated target not reached.
[^ladders]: Episodes AS-S11–AS-S14; live-results ledger. Probe-hop, GPU, and packing ladders in mid-August, all below the historical baseline and without matched controls.
[^memblind]: Episode OC-S02; quote Q05 ("do not trust the memory or recorded info, validate everything"). The memory-blind audit produced discipline, not a scored result.
[^standing]: Cutoff-2 and cutoff-3 live-results artifacts; episode AS-S15. Authenticated rank 171 of 4,186. The 173 of 4,251 silver report is testimony; no notification artifact survived audit.
[^reveal]: Episode AS-S17; cutoff-3 live-results artifact. The full retained submission population of 50 rows (one `ERROR`, 49 scored): 38 at exactly 0.000 private, 11 positive rows all from the confused-deputy line (2.290 to 16.805), none above 50 public scoring positive; selected Slot A `55766377` (92.670 public, 0.000 private) and Slot B `55805571` (16.555 public, 16.735 private).
[^frontier]: Episode AS-S16; cutoff-2 live-results artifact. No final-week attacker lever beat about 92.670; a direct query showed the public frontier at least 147.530 by 2026-08-29.
[^reset]: Episode ARC-S03. The between-plays reset probe showed a large local effect but returned an error in competition mode, making the test invalid for its claimed setting.
[^replay]: Episode ARC-S02. Search-and-replay solved all 25 development games locally; the scoring trick did not survive external conditions.
[^lora]: Episode ARC-S05; quote Q06 ("the LoRA never served; generation ran on base"). Treatment and control were the same served model; invalid experiment. The canonical file was missing at re-audit, so this rests on a prior ledger extract with repository corroboration.
[^prompt]: Episode ARC-S08. Prompt reduction raised the development mean but reversed on the hidden evaluation; a valid refuted transfer claim.
[^noise]: Episode ARC-S06. Same-versus-same replicates showed root-mean-square variation of about 0.707 game levels; two preregistered gates were underpowered and the protocol was amended.
[^perception]: Episodes ARC-S01, ARC-S07. Representation and parser work moved a retained comparison from 0/9 to 6/6, but role typing and masking changed together, so neither is isolated.
[^structural]: Episodes ARC-S09–ARC-S10; episode OC-S05. Structural planning, best-of-N selection, and a repaired memory strategy all stayed inside their established score bands.
[^corpus]: Episodes OC-S03–OC-S04. A nine-specialist search drew its corpus from the wrong model; breadth cannot repair provenance, so the episode is an invalid experiment, and a related unserved arm was killed before it spent a slot.
[^gate]: Quote Q07 ("serving identity proven first"); episode ARC-S05. The correction became a precondition for a claim rather than cleanup after a surprising score.
[^late]: Episodes ARC-S11–ARC-S12. A later engineered candidate did not replace the reference policy; a promising external model stayed open with no scored result by the cutoff.
[^copy]: Episode ARC-S13; cutoff-3 live-results artifact. A byte-for-byte copy of a credited public notebook scored 3.25 against a best in-house 1.94; most earlier record steps were exact-byte resubmissions, and the largest self-originated improvement was +0.14 (a model swap).
[^draws]: Episode ARC-S14; cutoff-3 live-results artifact. Identical submissions returned 3.25, 2.58, and an error; the one adjusted candidate returned 4.31 and 2.45.
[^rig]: Episodes ARC-S15–ARC-S16; cutoff-3 live-results artifact. On an off-platform rig with rules fixed before each run, a turn-budget change produced 118 levels against 118 despite large behavioural change, and a probe-discipline candidate returned 41 against a base of 39.33, inside its pre-declared dead band; both are local measurements, not live evidence, and the live confirmation was unfinished.
[^origins]: Public episode ledger, descriptive measures. Of 38 episodes: origins human 0, agent 16, external 4, mixed 18; statuses confirmed 8, partially supported 10, refuted 10, invalid experiment 5, superseded 1, open 4.
