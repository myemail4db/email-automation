# Real World Usage

## How this actually gets used

This is not something I run once and forget about.

It usually starts with emails coming in throughout the day. Some are useful, some are not, and after a while they all start to look the same.

Instead of trying to keep track in my inbox, I just label the ones I care about.

That label becomes the starting point.

---

## What I do first

I don’t touch the code. I don’t open any files.

I just go into Gmail and label a few emails:
```
for_friend
```

That’s it.

No formatting, no cleanup yet. Just marking what I want to process.

---

## Running the export

Then I run:

```bash
python -m src export --format text
```

This is where the shift happens.

Instead of reading emails one by one, the program pulls everything from that label and turns each email into its own file.

After it runs, I don’t look at Gmail anymore. I look at the folder:

```
processed_review/
```

That becomes my workspace.

---

## Reviewing the results

This part is important.

The files are usually close to what I want, but not perfect. Sometimes formatting is off. Sometimes there is extra text I don’t need.

So I open a few files, clean them up, and make sure they look right.

This step is quick, but I don’t skip it.

---

## Sending

Once everything looks good, I run:

```bash
python -m src send
```

At that point:
- the files are grouped into a batch
- the batch is sent
- the files are moved out of the review folder

Now the workspace is clean again.

---

## What makes this easier

The biggest difference is not speed.

It’s that I don’t have to remember anything.

I don’t have to think:
- did I already process this email?
- did I already send this one?
- what happened last time?

The folders and logs answer that for me.

---

## When something goes wrong

If something fails, it’s usually obvious.

Either:
- the file shows up in the error folder
- or the log tells me exactly where it stopped

I don’t have to dig through everything to figure it out.

---

## What this replaces

Before this, the process looked like this:
- open email
- copy content
- paste into a document
- rename the file
- repeat
- try to remember what was already done

Now it’s:
- label emails
- run export
- review
- send

That’s it.

---

## Final thought

This is not trying to automate everything.

It just removes the parts that were repetitive and hard to track.

Everything else stays simple.