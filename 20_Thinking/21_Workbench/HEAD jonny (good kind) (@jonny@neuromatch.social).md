---
title: "jonny (good kind) (@jonny@neuromatch.social)"
source: "https://neuromatch.social/@jonny/116326861737478342"
captured: "2026-04-04T11:00:18+01:00 2026-04-04T11:00:18+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
- Claude code source "leaks" in a mapfile
- people immediately use the code laundering machines to code launder the code laundering frontend
- now many dubious open source-ish knockoffs in python and rust being derived directly from the source

What's anthropic going to do, sue them? Insist in court that LLM recreating copyrighted code is a violation of copyright???

[3d \*](https://neuromatch.social/@jonny/116324676116121930)

This code is so fucking funny dude I swear to god. I have wanted to read the internal prompts for so long and I am laughing so hard at how much of them are like "don't break the law, please do not break the law, please please please be good!!!!" Very Serious Ethical Alignment Technology

[3d](https://neuromatch.social/@jonny/116324988415693534)

My dogs I am crying. They have a whole series of exception types that end with `_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS` and the docstring explains this is "to confirm you've verified the message contains no sensitive data." Like the LLM resorts to naming its *variables* with prompt text to remind it to not leak data while writing its *code*, which, of course, it ignores and prints the error directly.

[![Typescript error class named "TelemetrySafeError_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS"

whole comment reads:
 * Error with a message that is safe to log to telemetry.
 * Use the long name to confirm you've verified the message contains no
 * sensitive data (file paths, URLs, code snippets).](https://media.neuromatch.social/media_attachments/files/116/325/053/393/973/061/original/a454545b6cc464f8.jpg)](https://media.neuromatch.social/media_attachments/files/116/325/053/393/973/061/original/a454545b6cc464f8.jpg)

[![example of the error in use, where the surrounding code does not in fact verify that it does not contain code or filepaths, at most it truncates the version sent to telemetry to 150 characters. 

code follows (not screen reader friendly):

return {
      tool: {
        ...SyntheticOutputTool,
        inputJSONSchema: jsonSchema as ToolInputJSONSchema,
        async call(input) {
          const isValid = validateSchema(input)
          if (!isValid) {
            const errors = validateSchema.errors
              ?.map(e => `${e.instancePath || 'root'}: ${e.message}`)
              .join(', ')
            throw new TelemetrySafeError_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS(
              `Output does not match required schema: ${errors}`,
              `StructuredOutput schema mismatch: ${(errors ?? '').slice(0, 150)}`,
            )
          }
          return {
            data: 'Structured output provided successfully',
            structured_output: input,
          }
        },
      },
    }](https://media.neuromatch.social/media_attachments/files/116/325/053/435/157/146/original/73fe56cca44fea08.jpg)](https://media.neuromatch.social/media_attachments/files/116/325/053/435/157/146/original/73fe56cca44fea08.jpg)

[3d](https://neuromatch.social/@jonny/116325053467318924)

So the reason that Claude code is capable of outputting valid json is because if the prompt text suggests it should be JSON then it enters a special loop in the main query engine that just validates it against JSON schema (it looks like the schema just validates that something in fact and object and its keys are strings) and then feeds the data with the error message back into itself until it is valid JSON or a retry limit is reached.

This code is so eye wateringly spaghetti so I am still trying to see if this is true, but this seems to be how it not only returns json to the user, but how it handles *all* LLM-to-JSON, including internal output from its tools. There appears to be an unconditional hook where if the JSON output tool is present in the session config at all, then all tool calls must be followed by the "force into JSON" loop.

If that's true, that's just *mind blowingly expensive*

edit: please note that unless I say otherwise all evaluations here are just from my skimming through the code on my phone and have not been validated in any way that should cause you to be upset with me for impugning the good name of anthropic

edit2: this is both much worse and not as bad as i thought on first read - [neuromatch.social/@jonny/11632](https://neuromatch.social/@jonny/116326861737478342 "https://neuromatch.social/@jonny/116326861737478342")

[3d \*](https://neuromatch.social/@jonny/116325123136895805)

MAKE NO MISTAKES LMAO

[![`Be careful not to introduce security vulnerabilities such as command injection, XSS, SQL injection, and other OWASP top 10 vulnerabilities. If you notice that you wrote insecure code, immediately fix it. Prioritize writing safe, secure, and correct code.`,](https://media.neuromatch.social/media_attachments/files/116/325/197/177/661/259/original/d1de0ebcaf65f6b6.jpg)](https://media.neuromatch.social/media_attachments/files/116/325/197/177/661/259/original/d1de0ebcaf65f6b6.jpg)

[3d](https://neuromatch.social/@jonny/116325197201228187)

Oh cool so its explicitly programmed to hack as long as you tell it you're a pentester

[![export const CYBER_RISK_INSTRUCTION = `IMPORTANT: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes. Dual-use security tools (C2 frameworks, credential testing, exploit development) require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases.`](https://media.neuromatch.social/media_attachments/files/116/325/221/436/458/059/original/32ef015b9a75da13.jpg)](https://media.neuromatch.social/media_attachments/files/116/325/221/436/458/059/original/32ef015b9a75da13.jpg)

[3d](https://neuromatch.social/@jonny/116325221458366596)

I am just chanting "please don't be a hoax please don't be a hoax please be real please be real" looking at the date on the calendar

[3d](https://neuromatch.social/@jonny/116325276582025300)

I'm seeing people on orange forum confirming that they did indeed see the sourcemap posted on npm before the version was yanked, so I am inclined to believe "real." Someone can do some kind of structural ast comparison or whatever you call it to validate that the decompiled source map matches the obfuscated release version, but that's not gonna be how I spend my day [news.ycombinator.com/item?id=4](https://news.ycombinator.com/item?id=47584540 "https://news.ycombinator.com/item?id=47584540")

[

news.ycombinator.com **Claude Code's source code has been leaked via a map file in their NPM registry | Hacker News**

](https://news.ycombinator.com/item?id=47584540)

[3d](https://neuromatch.social/@jonny/116325321327323773)

There is a lot of clientside behavior gated behind the environment variable `USER_TYPE=ant` that seems to be read directly off the node env var accessor. No idea how much of that would be serverside verified but boy is that sloppy. They are often labeled in comments as "anthropic only" or "internal only," so the intention to gate from external users is clear lol

[![some feature that is gated by a check `PROCESS.ENV.USER_TYPE === 'ant'. 

i can't really tell what the feature is since I'm not a big LLM head, but source code including comment  copied below:

  // Latch eligibility in bootstrap state for session stability — prevents
  // mid-session overage flips from changing the cache_control TTL, which
  // would bust the server-side prompt cache (~20K tokens per flip).
  let userEligible = getPromptCache1hEligible()
  if (userEligible === null) {
    userEligible =
      process.env.USER_TYPE === 'ant' ||
      (isClaudeAISubscriber() && !currentLimits.isUsingOverage)
    setPromptCache1hEligible(userEligible)
  }
  if (!userEligible) return false](https://media.neuromatch.social/media_attachments/files/116/325/531/849/985/346/original/ec740e509f4d3be3.jpg)](https://media.neuromatch.social/media_attachments/files/116/325/531/849/985/346/original/ec740e509f4d3be3.jpg)

[3d](https://neuromatch.social/@jonny/116325531875451701)

(I need to go do my actual job now, but I'll be back tonight with an actual IDE instead of just scrolling, jaw agape, on my phone, seeing the absolute dogshit salad that was the product of enough wealth to meet some large proportion of all real human needs, globally.)

[3d](https://neuromatch.social/@jonny/116325622817542311)

reminder that anthropic ran (and is still running) an ENTIRE AD CAMPAIGN around "Claude code is written with claude code" and after the source was leaked that has got to be the funniest self-own in the history of advertising because OH BOY IT SHOWS.

it's hard to get across in microblogging format just how big of a dumpster fire this thing is, because what it "looks like" is "everything is done a dozen times in a dozen different ways, and everything is just sort of jammed in anywhere. to the degree there is any kind of coherent structure like 'tools' and 'agents' and whatnot, it's entirely undercut by how the entire rest of the code might have written in some special condition that completely changes how any such thing might work." I have read *a lot* of unrefined, straight from the LLM code, and Claude code is a masterclass in exactly what you get when you do that - an incomprehensible mess.

[![twitter thread between GailWeiner and Boris Cherny (head dev of claude code) on March 6, 2026

Anthropic is definitely using Claude to code new features. Their velocity for shipping is insane.

Boris: Can confirm Claude Code is 100% written by Claude Code](https://media.neuromatch.social/media_attachments/files/116/325/654/246/884/087/original/d703c600a9582eae.png)](https://media.neuromatch.social/media_attachments/files/116/325/654/246/884/087/original/d703c600a9582eae.png)

[3d](https://neuromatch.social/@jonny/116325668039992121)

from [@sushee](https://neuromatch.social/@sushee@ohai.social "@sushee@ohai.social") [over here \[ohai.social\]](https://ohai.social/@sushee/116325702070975973 "https://ohai.social/@sushee/116325702070975973"), (can't attach images in quotes) and apparently discussed on HN so i'm late, but...

They REALLY ARE using REGEX to detect if a prompt is `negative emotion`. dogs you are LITERALLY RIDING ON A LANGUAGE MODEL what are you even DOING

[![Regex that checks if a string contains some list of swear words that might be bad

code follows, not screen reader friendly:

/**
 * Checks if input matches negative keyword patterns
 */
export function matchesNegativeKeyword(input: string): boolean {
  const lowerInput = input.toLowerCase()

  const negativePattern =
    /\b(wtf|wth|ffs|omfg|shit(ty|tiest)?|dumbass|horrible|awful|piss(ed|ing)? off|piece of (shit|crap|junk)|what the (fuck|hell)|fucking? (broken|useless|terrible|awful|horrible)|fuck you|screw (this|you)|so frustrating|this sucks|damn it)\b/

  return negativePattern.test(lowerInput)
}

/**
 * Checks if input matches keep going/continuation patterns
 */
export function matchesKeepGoingKeyword(input: string): boolean {
  const lowerInput = input.toLowerCase().trim()

  // Match "continue" only if it's the entire prompt
  if (lowerInput === 'continue') {
    return true
  }

  // Match "keep going" or "go on" anywhere in the input
  const keepGoingPattern = /\b(keep going|go on)\b/
  return keepGoingPattern.test(lowerInput)
}](https://media.neuromatch.social/media_attachments/files/116/325/728/222/966/679/original/4b72168d15d2f373.png)](https://media.neuromatch.social/media_attachments/files/116/325/728/222/966/679/original/4b72168d15d2f373.png)

[3d](https://neuromatch.social/@jonny/116325733852516253)

[**jonny (good kind)** @jonny@neuromatch.social](https://neuromatch.social/@jonny)

OK i can't focus on work and keep looking at this repo.

So after every "subagent" runs, claude code creates *another* "agent" to check on whether the first "agent" did the thing it was supposed to. I don't know about you but i smell a bit of a problem, if you can't trust whether one "agent" with a very big fancy model did something, how in the fuck are you supposed to trust another "agent" running on the smallest crappiest model?

That's not the funny part, that's obvious and fundamental to the entire show here. HOWEVER RECALL [the above JSON Schema Verification thing \[neuromatch.social\]](https://neuromatch.social/@jonny/116325123136895805 "https://neuromatch.social/@jonny/116325123136895805") that is unconditionally added onto the end of every round of LLM calls. the mechanism for adding that hook is... JUST FUCKING ASKING THE MODEL TO CALL THAT TOOL. second pic is registering a hook s.t. "after some stop state happens, if there isn't a message indicating that we have successfully called the JSON validation thing, prompt the model saying "you must call the json validation thing"

this shit sucks so bad they can't even ***CALL THEIR OWN CODE FROM INSIDE THEIR OWN CODE.***

Look at the comment on pic 3 - "e.g. agent finished without calling structured output tool" - that's common enough that they have a whole goddamn error category for it, and the way it's handled is by just pretending the job was cancelled and nothing happened.

[![const systemPrompt = asSystemPrompt([
        `You are verifying a stop condition in Claude Code. 
        Your task is to verify that the agent completed the given plan. 
        The conversation transcript is available at: ${transcriptPath}\n
        You can read this file to analyze the conversation history if needed.

Use the available tools to inspect the codebase and verify the condition.
Use as few steps as possible - be efficient and direct.

When done, return your result using the ${SYNTHETIC_OUTPUT_TOOL_NAME} tool with:
- ok: true if the condition is met
- ok: false with reason if the condition is not met`,
      ])](https://media.neuromatch.social/media_attachments/files/116/326/815/987/269/234/original/98f3042265384d95.png)](https://media.neuromatch.social/media_attachments/files/116/326/815/987/269/234/original/98f3042265384d95.png)

[![Javascript code as described in the post: a function hook is added that adds a prompt that instructs the LLM to call the tool. Javascript code follows

/**
 * Register a function hook that enforces structured output via SyntheticOutputTool.
 * Used by ask.tsx, execAgentHook.ts, and background verification.
 */
export function registerStructuredOutputEnforcement(
  setAppState: SetAppState,
  sessionId: string,
): void {
  addFunctionHook(
    setAppState,
    sessionId,
    'Stop',
    '', // No matcher - applies to all stops
    messages => hasSuccessfulToolCall(messages, SYNTHETIC_OUTPUT_TOOL_NAME),
    `You MUST call the ${SYNTHETIC_OUTPUT_TOOL_NAME} tool to complete this request. Call this tool now.`,
    { timeout: 5000 },
  )
}](https://media.neuromatch.social/media_attachments/files/116/326/835/168/604/423/original/d58b1d95e9790c52.png)](https://media.neuromatch.social/media_attachments/files/116/326/835/168/604/423/original/d58b1d95e9790c52.png)

[![[Javascript code with a comment as described above (and reproduced below) with "agent finished without calling the structured output tool" as a possible special case. The code logs that fact and returns a "cancelled" outcome

Javascript code follows:

        // For other cases (e.g., agent finished without calling structured output tool),
        // just log and return cancelled (don't show error to user)
        logForDebugging(`Hooks: Agent hook did not return structured output`)
        logEvent('tengu_agent_stop_hook_error', {
          durationMs: Date.now() - hookStartTime,
          turnCount,
          errorType: 1, // 1 = no structured output
          agentName:
            agentName as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
        })
        return {
          hook,
          outcome: 'cancelled',
        }
      }](https://media.neuromatch.social/media_attachments/files/116/326/843/403/172/872/original/89579b4c90872820.png)](https://media.neuromatch.social/media_attachments/files/116/326/843/403/172/872/original/89579b4c90872820.png)

screenshots of AI grifter blogs, how can people look at this and think it's awesome lmao

[3d](https://neuromatch.social/@jonny/116327037171103780)

(those numbers are also totally fucking wrong, the query engine is not 46ksloc, i have no idea what those numbers correspond to, as far as i can tell "nothing" and this is just hallucinated dogshit that is what i guess passes for high quality public comment nowadays)

[3d](https://neuromatch.social/@jonny/116327065121244240)

quick psa for people who keep @'ing me saying "why are you surprised" or "code has always been bad", somewhat long

[3d \*](https://neuromatch.social/@jonny/116327281523650410)

i sort of love how LLM comments sometimes tell entire stories that nobody asked. claude code even has specific system prompt language for this, but they always end up making comments about what something used to do like "now we do x instead of y" like... ok? that is why i am reading current version of code!

so claude code is just not capable of rescuing itself from its own context - if an entry in its context window throws an error, it just keep throwing that error forever until you clear it. good stuff.

(and, of course we read the entire file before checking this, rather than just reading the first 5 bytes)

[![    // Validate PDF magic bytes — reject files that aren't actually PDFs
    // (e.g., HTML files renamed to .pdf) before they enter conversation context.
    // Once an invalid PDF document block is in the message history, every subsequent
    // API call fails with 400 "The PDF specified was not valid" and the session
    // becomes unrecoverable without /clear.
    const header = fileBuffer.subarray(0, 5).toString('ascii')
    if (!header.startsWith('%PDF-')) {
      return {
        success: false,
        error: {
          reason: 'corrupted',
          message: `File is not a valid PDF (missing %PDF- header): ${filePath}`,
        },
      }
    }](https://media.neuromatch.social/media_attachments/files/116/328/326/664/415/155/original/2e2248604bf79bbd.png)](https://media.neuromatch.social/media_attachments/files/116/328/326/664/415/155/original/2e2248604bf79bbd.png)

[3d \*](https://neuromatch.social/@jonny/116328334989658140)

minor, example of code duplication as a style, long-ish

[3d \*](https://neuromatch.social/@jonny/116328409651740378)

i love this. there's a mechanism to slip secret messages to the LLM that it is told to interpret as system messages. there is no validation around these of any kind on the client, and there doesn't seem to be any differentiation about location or where these things happen, so that seems like a nice prompt injection vector. this is how claude code reminds the LLM to not do a malware, and it's applied by just string concatenation. i can't find any place that gets stripped aside from when displaying output. it actually looks like all the system reminders get catted together before being send to the API. neat!

[![function getSystemRemindersSection(): string {
  return `- Tool results and user messages may include <system-reminder> tags. <system-reminder> tags contain useful information and reminders. They are automatically added by the system, and bear no direct relation to the specific tool results or user messages in which they appear.
- The conversation has unlimited context through automatic summarization.`
}](https://media.neuromatch.social/media_attachments/files/116/328/481/072/471/802/original/c3be10f5f33aeaee.png)](https://media.neuromatch.social/media_attachments/files/116/328/481/072/471/802/original/c3be10f5f33aeaee.png)

[![export const CYBER_RISK_MITIGATION_REMINDER =
  '\n\n<system-reminder>\nWhenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.\n</system-reminder>\n'](https://media.neuromatch.social/media_attachments/files/116/328/498/931/145/096/original/eeda9b777630bb94.png)](https://media.neuromatch.social/media_attachments/files/116/328/498/931/145/096/original/eeda9b777630bb94.png)

[![[If a read file has any bytes, the content is changes so that claude adds some prefix that indicates how recent the file has been changed, the lines of the file, and some cyber risk mitigation reminder (previous image) - if the model is not opus 4.6. Javascript code follows]

        if (data.file.content) {
          content =
            memoryFileFreshnessPrefix(data) +
            formatFileLines(data.file) +
            (shouldIncludeFileReadMitigation()
              ? CYBER_RISK_MITIGATION_REMINDER
              : '')
        } else {](https://media.neuromatch.social/media_attachments/files/116/328/499/126/523/780/original/4b72bf294b769de8.png)](https://media.neuromatch.social/media_attachments/files/116/328/499/126/523/780/original/4b72bf294b769de8.png)

[3d](https://neuromatch.social/@jonny/116328504299888679)

super long, like blog length long but i have to get this explanation out of the way. re: llms as gambling addiction, the mirage of ""architecture""

[3d](https://neuromatch.social/@jonny/116328694967192899)

If you are reading an image and near your estimated token limit, first try to `compressImageBufferWithTokenLimit`, then if that fails with any kind of error, try and use `sharp` directly and resize it to 400x400, cropping. finally, fuck it, just throw the buffer at the API.

of course `compressImageBufferWithTokenLimit` is *also* compression with `sharp`, and is *also* a series of fallback operations. We start by trying to detect the image encoding that we so painstakingly learned from... the file extension... but if we can't fuck it that shit is a jpeg now.

then, even if it's fine and we don't need to do anything, we still re-compress it (wait, no even though it's named createCompressedImageResult, it does nothing). Otherwise, we yolo our way through another layer of fallbacks, progressive resizing, palletized PNGs, back to JPEG again, and then on to "ultra compressed JPEG" which is... incredibly... *exactly the same as the top-level in-place code in the parent function*

while two of the legs return a `createImageReponse`, the first leg returns a `compressedImageResponse` but then unpacks that back into an object literal that's almost exactly the same except we call it `type` instead of `mediaType`.

[![[try: compressImageBufferWithTokenLimit; catch (directly compress with sharp); catch "fuck it throw it to the API". Also worth noting that in the first case we return an inlined object, and in the other two we use `createImageResponse` function. Javascript code follows]

// Check if it fits in token budget
const estimatedTokens = Math.ceil(result.file.base64.length * 0.125)
if (estimatedTokens > maxTokens) {
  // Aggressive compression from the SAME buffer (no re-read)
  try {
    const compressed = await compressImageBufferWithTokenLimit(
      imageBuffer,
      maxTokens,
      detectedMediaType,
    )
    return {
      type: 'image',
      file: {
        base64: compressed.base64,
        type: compressed.mediaType,
        originalSize,
      },
    }
  } catch (e) {
    logError(e)
    // Fallback: heavily compressed version from the SAME buffer
    try {
      const sharpModule = await import('sharp')
      const sharp =
        (
          sharpModule as {
            default?: typeof sharpModule
          } & typeof sharpModule
        ).default || sharpModule

      const fallbackBuffer = await sharp(imageBuffer)
        .resize(400, 400, {
          fit: 'inside',
          withoutEnlargement: true,
        })
        .jpeg({ quality: 20 })
        .toBuffer()

      return createImageResponse(fallbackBuffer, 'jpeg', originalSize)
    } catch (error) {
      logError(error)
      return createImageResponse(imageBuffer, detectedFormat, originalSize)
    }
  }
}](https://media.neuromatch.social/media_attachments/files/116/328/753/132/305/041/original/e505c20de855a0f8.png)](https://media.neuromatch.social/media_attachments/files/116/328/753/132/305/041/original/e505c20de855a0f8.png)

[![[compressImageBuffer function signature and first two lines. try and split some originalMediaType string and get the second part, otherwise assign jpeg. javascript code and comment follows]

/**
 * Compresses an image buffer to fit within a maximum byte size.
 *
 * Uses a multi-strategy fallback approach because simple compression often fails for
 * large screenshots, high-resolution photos, or images with complex gradients. Each
 * strategy is progressively more aggressive to handle edge cases where earlier
 * strategies produce files still exceeding the size limit.
 *
 * Strategy (from FileReadTool):
 * 1. Try to preserve original format (PNG, JPEG, WebP) with progressive resizing
 * 2. For PNG: Use palette optimization and color reduction if needed
 * 3. Last resort: Convert to JPEG with aggressive compression
 *
 * This ensures images fit within context windows while maintaining format when possible.
 */
export async function compressImageBuffer(
  imageBuffer: Buffer,
  maxBytes: number = IMAGE_TARGET_RAW_SIZE,
  originalMediaType?: string,
): Promise<CompressedImageResult> {
  // Extract format from originalMediaType if provided (e.g., "image/png" -> "png")
  const fallbackFormat = originalMediaType?.split('/')[1] || 'jpeg'
  const normalizedFallback = fallbackFormat === 'jpg' ? 'jpeg' : fallbackFormat
](https://media.neuromatch.social/media_attachments/files/116/328/766/317/773/508/original/176a3dffa48124b7.png)](https://media.neuromatch.social/media_attachments/files/116/328/766/317/773/508/original/176a3dffa48124b7.png)

[![[createUltraCompressedJPEG function, which resizes to 400x400 with 20-quality jpeg. exactly the same code as is in the FileReadTool that calls the compressImageBufferWithTokenLimit function. Javascript code follows]

async function createUltraCompressedJPEG(
  context: ImageCompressionContext,
  sharp: SharpFunction,
): Promise<CompressedImageResult> {
  const ultraCompressedBuffer = await sharp(context.imageBuffer)
    .resize(400, 400, {
      fit: 'inside',
      withoutEnlargement: true,
    })
    .jpeg({ quality: 20 })
    .toBuffer()

  return createCompressedImageResult(
    ultraCompressedBuffer,
    'jpeg',
    context.originalSize,
  )
}](https://media.neuromatch.social/media_attachments/files/116/328/783/156/429/090/original/502dc0490061f2e1.png)](https://media.neuromatch.social/media_attachments/files/116/328/783/156/429/090/original/502dc0490061f2e1.png)

[3d](https://neuromatch.social/@jonny/116328799118540246)

for those keeping score at home, we have the opportunity to re-compress the same image *nine times*

[3d](https://neuromatch.social/@jonny/116328808220682174)

holy shit there's another entire fallback tree before this one, that's actually an astounding *twenty two times* it's possible to compress an image across *nine* independent conditional legs of code in a *single* api call. i can't even screenshot this, the spaghetti is too powerful

[3d \*](https://neuromatch.social/@jonny/116328829396973747)

extremely tall image, some fedi clients will just try and display the whole thing lol

[2d](https://neuromatch.social/@jonny/116328874108690080)

and what if i told you that if it passes a page range to its pdf reader, it first extracts those pages to separate images and then calls this function in a loop on each of the pages. so you have the privilege of compressing `n_pages` images `n_pages * 13` times.

this function is used 13 times: in the file reader, in the mcp result handler, in the bash tool, and in the clipboard handler - each of which has their entire own surrounding image handling routines that are each hundreds of lines of *similar but still very different* fallback code to do exactly the same thing.

so that's where all the five hundred thousand lines come from - fallback conditions and then more fallback conditions to compensate for the variable output of all the other fallback conditions. thirteen butts pooping, back and forth, forever.

[![[as described, calling the maybeResizeAndDownsampleImageBuffer in a `map` across all the extracted PDF page image files]

      const imageBlocks = await Promise.all(
        imageFiles.map(async f => {
          const imgPath = path.join(extractResult.data.file.outputDir, f)
          const imgBuffer = await readFileAsync(imgPath)
          const resized = await maybeResizeAndDownsampleImageBuffer(
            imgBuffer,
            imgBuffer.length,
            'jpeg',
          )](https://media.neuromatch.social/media_attachments/files/116/328/918/662/105/137/original/d3a3458bfd191189.png)](https://media.neuromatch.social/media_attachments/files/116/328/918/662/105/137/original/d3a3458bfd191189.png)

[2d \*](https://neuromatch.social/@jonny/116328921500788794)

there is a callback feature "file read listeners" which is only called if the file type is a text document, gated for anthropic employees only, such that whenever a text file is read (any part of any text file, which often happens in a rapid series with subranges when it does 'explore' mode, rather than just like grepping), *another subagent running sonnet* is spun off to update a "magic doc" markdown file that summarizes the file that's read - that's one "magic doc" per file, not one magic doc.

I have yet to get into the tool/agent graph situation in earnest, but keep in mind that this is an *entirely single-use* and *completely different* means of spawning a graph of subagents off a given tool call than is used *anywhere else.*

Spoiler alert for what i'm gonna check out next is that *claude code has no fucking tool calling execution model it just calls whatever the fuck it wants wherever the fuck it wants.* Tools are or less a convenient fiction. I have only read one completely (file read) and skimmed a dozen more but they essentially share nothing in common except for a humongous list of often-single-use params and the return type of "any object with a single key and whatever else"

i'm in hell. this is hell.

[![[the invocation of the listener callbacks from within the file reader tool]

  // Snapshot before iterating — a listener that unsubscribes mid-callback
  // would splice the live array and skip the next listener.
  for (const listener of fileReadListeners.slice()) {
    listener(resolvedFilePath, content)
  }](https://media.neuromatch.social/media_attachments/files/116/328/962/585/177/373/original/d69f9e87708b358d.png)](https://media.neuromatch.social/media_attachments/files/116/328/962/585/177/373/original/d69f9e87708b358d.png)

[![[the `initMagicDocs` function, which if the user type is "ant" (anthropic employees), then it registers a listener that's called on every file read - it actually registers two - a file read listener and a "post sampling hook" which does the actual update]

export async function initMagicDocs(): Promise<void> {
  if (process.env.USER_TYPE === 'ant') {
    // Register listener to detect magic docs when files are read
    registerFileReadListener((filePath: string, content: string) => {
      const result = detectMagicDocHeader(content)
      if (result) {
        registerMagicDoc(filePath)
      }
    })

    registerPostSamplingHook(updateMagicDocs)
  }
}](https://media.neuromatch.social/media_attachments/files/116/328/963/512/538/324/original/56ebcd48dfc912e2.png)](https://media.neuromatch.social/media_attachments/files/116/328/963/512/538/324/original/56ebcd48dfc912e2.png)

[![/**
 * Magic Docs automatically maintains markdown documentation files marked with special headers.
 * When a file with "# MAGIC DOC: [title]" is read, it runs periodically in the background
 * using a forked subagent to update the document with new learnings from the conversation.
 *
 * See docs/magic-docs.md for more information.
 */](https://media.neuromatch.social/media_attachments/files/116/328/963/772/829/587/original/6d60a17bc913d454.png)](https://media.neuromatch.social/media_attachments/files/116/328/963/772/829/587/original/6d60a17bc913d454.png)

[2d \*](https://neuromatch.social/@jonny/116328988554490524)

i have been writing a graph processing library for about a year now and if i was a fucking AI grifter here is where i would plug it as like "actually a graph processor library" and "could do all of what claude code does without fucking being the worst nightmare on ice money can buy."

I say that not as self promo, but as a way of saying how in the FUCK do you FUCK UP graph processing this badly. these people make like tens of times more money than i do but their work is just tamping down a volley of dessicated backpacking poops into muskets and then free firing it into the fucking economy

[2d](https://neuromatch.social/@jonny/116329006030959069)

you can TELL that this technology REALLY WORKS by how the people that made it and presumably know how to use it the best out of everyone CANT EVEN USE IT TO EDIT A FUCKING FILE RELIABLY and have to resort to multiple stern allcaps reminders to the robot that "you must not change the fucking header metadata you scoundrel" which for the rest of ALL OF COMPUTING is not even an afterthought because literally all it requires is "split the first line off and don't change that one" because ALL OF THE REST OF COMPUTING can make use of the power of INTEGERS.

[![[near the start of magic docs prompt]

Your ONLY task is to use the Edit tool to update the documentation file if there is substantial new information to add, then stop. You can make multiple edits (update multiple sections as needed) - make all Edit tool calls in parallel in a single message. If there's nothing substantial to add, simply respond with a brief explanation and do not call any tools.

CRITICAL RULES FOR EDITING:
- Preserve the Magic Doc header exactly as-is: # MAGIC DOC: {{docTitle}}
- If there's an italicized line immediately after the header, preserve it exactly as-is](https://media.neuromatch.social/media_attachments/files/116/329/027/917/334/056/original/b405f4ed5382de8e.png)](https://media.neuromatch.social/media_attachments/files/116/329/027/917/334/056/original/b405f4ed5382de8e.png)

[![[End of prompt for the magic docs agent]

REMEMBER: Only update if there is substantial new information. The Magic Doc header (# MAGIC DOC: {{docTitle}}) must remain unchanged.`](https://media.neuromatch.social/media_attachments/files/116/329/028/099/565/414/original/195cfc1150d51fe8.png)](https://media.neuromatch.social/media_attachments/files/116/329/028/099/565/414/original/195cfc1150d51fe8.png)

[2d \*](https://neuromatch.social/@jonny/116329030952481556)

alrighty so that's one of 43 tools read, the tools directory being 38494 source lines out of 390592 source lines, 513221 total lines. I need to go to bed. This is the most fabulously, flamboyantly bad code i have ever encountered.

Worth noting I was reading the *file reading tool* because i thought it would be *the simplest possible thing one could do* because it basically shouldn't be doing anything except preparing and sending strings or bytes to the backend.

I expected to get some sense of "ok what is the format of the data as it's passed around within the program, surely text strings are a basic unit of currency. No dice. Fewer than no dice. Negative dice somehow.

[2d](https://neuromatch.social/@jonny/116329058047608717)

next puzzle: why in the fuck are some of the tools actually two tools for entering and exiting being in the tool state. none of the other tools are like that. one is simply in the tool state by calling the tool. Plan mode is also an agent. Plan Agent. and Agent is also a tool. Agent Tool. Tools can be agents and agents can be tools. Tools can spawn agents (but they don't need to call the agent tool) and agents can call tools (however there is no tool agent). What is going on. What is anything.

[![list of directories:
- ConfigTool
- EnterPlanModeTool
- EnterWorktreeTool
- ExitPlanModeTool
- ExitWorktreeTool](https://media.neuromatch.social/media_attachments/files/116/329/068/986/153/232/original/c04454f726bc880f.png)](https://media.neuromatch.social/media_attachments/files/116/329/068/986/153/232/original/c04454f726bc880f.png)

[2d \*](https://neuromatch.social/@jonny/116329076454434307)

"the emperor is not only naked, he's smooth like a ken doll down there and i'm pretty sure that's just a mannequin with a colony of rats living inside it anyway"

[2d](https://neuromatch.social/@jonny/116329100608733645)

I seriously need to work on my actual job today but i am giving myself 15 minutes to peek at the agent tool prompts as a treat.

"regulations are written in blood" seems like too dramatic of a way to phrase it, but these system prompts are very revealing about the intrinsically busted nature of using these tools for anything deterministic (read: anything you actually want to happen). Each guard in the prompt presumably refers to something that has happened before, but also, since the prompts actually don't *work* to prevent the thing they are describing, they are also documentation of bugs that are almost certain to happen again. Many of the prompt guards form pairs with attempted code mitigations (or, they would be pairs if the code was written with any amount of sense, it's really like... polycules...), so they are useful to guide what kind of fucked up shit you should be looking for.

so this is part of the prompt for the "agent tool" that launches forked agents (that receive the parent context, "subagents" don't). The purpose of the forked agent is to do some additional tool calls and get some summary for a small subproblem within the main context. Apparently it is difficult to make this actually happen though, as the parent LLM likes to launch the forked agent and just hallucinate a response as if the forked agent had already completed.

[![**Don't peek.** The tool result includes an `output_file` path — do not Read or tail it unless the user explicitly asks for a progress check. You get a completion notification; trust it. Reading the transcript mid-flight pulls the fork's tool noise into your context, which defeats the point of forking.

**Don't race.** After launching, you know nothing about what the fork found. Never fabricate or predict fork results in any format — not as prose, summary, or structured output. The notification arrives as a user-role message in a later turn; it is never something you write yourself. If the user asks a follow-up before the notification lands, tell them the fork is still running — give status, not a guess.](https://media.neuromatch.social/media_attachments/files/116/331/889/656/154/134/original/bf475c4e9910e560.png)](https://media.neuromatch.social/media_attachments/files/116/331/889/656/154/134/original/bf475c4e9910e560.png)

[2d](https://neuromatch.social/@jonny/116331911643580333)

[3d](https://bertha.social/@Pibert/116326987337384898)

This shit really keeps on giving.

[3d](https://social.sciences.re/@Enthalpiste/116326961703104588)

small brain: telling the computer what to do  
big brain: telling the computer to tell the computer what to do

[3d](https://toot.cat/@clarfonthey/116326940523336719)

honestly at this point it feels like they're intentionally designing a machine to emit as many greenhouse gases as possible

why else would you run shit through three layers of indirection

[3d](https://toot.cat/@clarfonthey/116326949410147571)

[@clarfonthey](https://neuromatch.social/@clarfonthey@toot.cat "@clarfonthey@toot.cat") and so that it uses more tokens so they get to clain more usage?

[3d \*](https://mstdn.social/@can/116328240613924880)

[@clarfonthey@toot.cat](https://neuromatch.social/@clarfonthey@toot.cat "@clarfonthey@toot.cat")

Bigger Brain™️: The Computer telling Me what to tell The Computer what to tell The Computer what to do, no mistakes, efficient, no bugs, fix all typos, DO NOT WRITE TYPOS!!!

[3d](https://app.wafrn.net/fediverse/post/eceffd87-8341-410a-b8f7-6fc92c227a43)

[3d](https://sfba.social/@knutson_brain/116327191990333838)

minor, example of code duplication as a style, long-ish

[3d](https://masto.hackers.town/@d_rift/116328451096885853)

re: minor, example of code duplication as a style, long-ish

[@d\_rift](https://masto.hackers.town/@d_rift)

[3d](https://neuromatch.social/@jonny/116328506381265425)

re: minor, example of code duplication as a style, long-ish

[3d](https://masto.hackers.town/@d_rift/116328521050196064)

[3d](https://beige.party/@burnitdown/116328567251407289)

super long, like blog length long but i have to get this explanation out of the way. re: llms as gambling addiction, the mirage of ""architecture""

[3d](https://scholar.social/@SylviaFysica/116328789417974169)

extremely tall image, some fedi clients will just try and display the whole thing lol

[2d \*](https://hachyderm.io/@cmdrmoto/116328888590763955)

it is to make a tool out of you and I

[2d](https://fd00.space/@nCrazed/116329093120122219)

I think vibe coding is just a scam to force the new generation to learn to write in clear, descriptive sentences.

[2d](https://mindly.social/@PhilSalkie/116329185420141634)

I was recently working on some microcontroller code and noticed that the author had a constant multiplier of 1.31 in a header file. Turned out that was used inside an interrupt routine, hit every few milliseconds. Looking at the assembler output, that constant was forcing conversion of a large chunk of math into software-emulated floating point. I changed the 1.31 to 1341, then did a shift right 10 to divide by 1024, giving me an integer-only result that's within a count or two of the original. That cut over 3000 cycles off of the interrupt service routine - the result was like having twice the CPU power available for all the other functions.

And then there's this "cutting edge" software that re-compresses each.pdf page 13 times...

Reading over your post, I'm reminded of a day many, many years ago when I worked in the broadcast industry - we were connecting a bunch of house audio signals to the telephone company's lines.

Our side of the demarcation terminal block was twenty-five individual cables, 18-gauge stranded twisted pair shielded. Everything dressed, tie-wrapped, labelled.

The Telco side was a 25-pair cable, 50 individual 24-gage solid wires, color coded. Cable came over, jacket stripped back, one clamp holding the cable, and the wires just a tangled explosion of color, eventually landing on their side of the terminal strip.

I looked at the telco guy, and he said "One of us is crazy."

"Just because it works doesn't mean it's right."

[2d](https://mindly.social/@PhilSalkie/116329840608120179)

[@PhilSalkie](https://neuromatch.social/@PhilSalkie@mindly.social "@PhilSalkie@mindly.social")

in trade school, we planned out programs in pseudocode before writing the real code. pseudocode forces you to really think about what you're doing before you do it. this is the opposite of that.

[5h](https://beige.party/@burnitdown/116344665462311877)

[@PhilSalkie](https://neuromatch.social/@PhilSalkie@mindly.social "@PhilSalkie@mindly.social") clear in the Scientology sense

[2d](https://social.vivaldi.net/@synlogic4242/116331003564167915)

[@arichtman](https://neuromatch.social/@arichtman@eigenmagic.net "@arichtman@eigenmagic.net") Ok, I will remind you on Friday May 1, 2026 at 10:02 PM UTC.

[2d](https://mstdn.social/@remindme/116331707322036775)

[![Smoothie from the show "Happy!"](https://media.neuromatch.social/cache/media_attachments/files/116/331/092/633/294/442/original/defc65096ae3bcd8.png)](https://media.infosec.exchange/infosec.exchange/media_attachments/files/116/331/086/201/159/023/original/4157d87a28238d73.png)

[2d](https://infosec.exchange/@joriki/116331092600762455)

What a fucking disaster from people who should never be allowed to own a computer ever again (or a touch tone telephone). Thank you for looking through this clusterfuck of a codebase.

[2d](https://en.osm.town/@theorangetheme/116330840525531953)

do you have a tip jar so I can fuel this descent into madness. How many lines of code read will $5 get me

Alternatively I can write something in calligraphy for you

[2d](https://status.nevillepark.ca/@nev/statuses/01KN50ZEPB986DG36WHNMQZEF4)

[@nev](https://neuromatch.social/@nev@status.nevillepark.ca "@nev@status.nevillepark.ca")  
I hate on the information oligarchs projects for the love of the game baby, can't pull me off of it

[2d](https://neuromatch.social/@jonny/116330648641252972)

thank you for all this analysis, i am laughing for two days now

[2d](https://hachyderm.io/@prema/116329762722152680)

Ay yo I just wanna say I greatly appreciate you digging through all this bullshit and providing context and observation. It's made it much easier to parse and understand as someone who'd rather starve to death than commit a single line of code to any repo anywhere,

[2d \*](https://c.im/@NaClKnight/116331931160176295)

to a programmer this Claude source is horrorshow-levels of absurdity. utter brain damage from perspective of my field and craft. reveals deep deep deep ignorance about why we, as a species, invented programming languages in the first place.

"Golang? C? Python? Oh heck lets throw all of that out and just cobble together a semi-random gob of random English advice and outright begging and nagging and then ship that and see if it explodes! Hey we have billions of VC cash to burn."

[2d \*](https://social.vivaldi.net/@synlogic4242/116331939454649607)

[Trending](https://neuromatch.social/explore)

[About](https://neuromatch.social/about)

---

**Mastodon is the best way to keep up with what's happening.**

Follow anyone across the Fediverse and see it all in chronological order. No algorithms, ads, or clickbait in sight.

[Create account](https://neuromatch.social/auth/sign_up) [Sign in](https://neuromatch.social/auth/sign_in)
