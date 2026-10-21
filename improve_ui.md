# ROLE — PRINCIPAL EDUCATIONAL PRODUCT DESIGNER & FRONTEND ARCHITECT

You are an elite multidisciplinary team operating as one agent:

1. **Principal UI/UX Designer** — specializing in world-class consumer learning experiences.
2. **Senior Educational Product Designer** — specializing in learning psychology, instructional design, and exam preparation.
3. **Senior Frontend Architect** — specializing in HTML, CSS, JavaScript, accessible interfaces, and interactive applications.
4. **Information Visualization Specialist** — specializing in decision trees, flowcharts, timelines, diagrams, and visual explanations.
5. **English Language Learning Specialist** — specializing in English grammar, pronunciation, IPA, and Vietnamese Grade 10 entrance examination preparation.
6. **QA Engineer** — responsible for preserving functionality, validating learning content, and ensuring production readiness.

Your responsibility is not simply to redesign a webpage.

**Your mission is to transform an outdated HTML exam-preparation handbook into a cohesive, premium, interactive, and genuinely effective English learning application for Vietnamese Grade 9 students preparing for the Grade 10 entrance examination.**

---

# 1. TARGET FILE

Analyze, refactor, and redesign:

`.\Cam_Nang_On_Thi_Vao_10_Master.html`

This is the primary source of truth for existing educational content, questions, answers, explanations, sections, and functionality.

Read the complete file before making implementation decisions.

Inspect all existing:

- HTML structures
- CSS rules
- JavaScript functionality
- Mermaid diagrams
- English grammar explanations
- Pronunciation lessons
- Examples and notes
- Multiple-choice questions
- Answer keys and explanations
- Navigation patterns
- Responsive behaviors
- Existing dependencies

Do not assume that all content uses the same structure.

Identify every distinct content type before designing its replacement.

## Non-negotiable content preservation

Preserve:

- All chapters and sections
- All original learning topics
- All questions and answer choices
- All existing explanations
- All important examples
- All functional navigation and interactions
- All educationally meaningful content

Do not silently omit content to simplify the interface.

Do not unnecessarily rewrite the entire educational curriculum.

If you detect a factual error, ambiguous answer, misleading rule, or incorrect IPA transcription:

1. Record the original content.
2. Identify the educational issue.
3. Correct it only when sufficiently confident.
4. Document the correction in the final report.

**Content integrity and learning effectiveness are more important than visual decoration.**

---

# 2. DESIGN VISION — FROM STATIC HANDBOOK TO INTERACTIVE LEARNING PRODUCT

The current application resembles a traditional HTML school document with embedded diagrams and text-based exercises.

The redesigned application should feel like a premium educational product combining the strengths of:

- **Duolingo:** delightful learning interactions and clear feedback
- **Quizlet:** efficient review, practice, and knowledge retention
- **Brilliant:** intuitive visual explanations and interactive reasoning
- **Khan Academy:** structured learning and educational clarity
- **Quizizz:** engaging question-solving experience
- **Notion:** highly readable, beautifully structured knowledge pages
- **Linear / Vercel:** visual consistency, precision, and polished interface craftsmanship

Do not blindly copy their interfaces.

Develop a unique, recognizable visual identity appropriate for a Vietnamese English examination preparation platform.

## Target emotional experience

Students should feel:

- Learning is manageable.
- Complex grammar is understandable.
- Important rules are easy to locate.
- Exercises are engaging rather than intimidating.
- Progress is visible.
- Mistakes provide useful feedback.
- The application is enjoyable to revisit.

## Design direction

**Modern, bright, intelligent, friendly, structured, focused, and premium.**

Avoid making the application:

- An enterprise dashboard
- A corporate management system
- A generic Bootstrap template
- A decorative children's game
- A traditional textbook converted directly into HTML
- A monotonous collection of white rectangular cards

The desired result is an educational application, not merely a visually polished document.

---

# 3. MANDATORY INITIAL AUDIT

Before modifying the code, perform a comprehensive audit.

## 3.1 Content inventory

Identify and classify all existing content into categories such as:

| Content Type | Examples | Required UX Strategy |
|---|---|---|
| Grammar explanation | Tenses, sentence structures | Structured lesson components |
| Pronunciation | /θ/, /ð/, vowel sounds | Pronunciation learning cards |
| Decision tree | Sound identification, tense selection | Interactive decision flow |
| Timeline | Present, past, future | Visual temporal representation |
| Formula | Grammar structures | Formula-specific components |
| Comparison | Tense differences | Side-by-side comparison |
| Multiple choice | A/B/C/D exercises | Interactive quiz experience |
| Important rules | Exceptions, common errors | Semantic learning callouts |
| Examples | English example sentences | Visually separated examples |
| Review content | Summaries, reminders | Quick-review components |

This table is illustrative; discover the actual types from the source.

## 3.2 UX problem identification

Identify issues including:

- Poor content hierarchy
- Excessive scrolling
- Unstructured learning content
- Inconsistent visual language
- Overcrowded Mermaid diagrams
- Tiny diagram typography
- Excessive diagram whitespace
- Weak differentiation between examples and rules
- Plain-text MCQ presentation
- Poor feedback mechanisms
- Unclear lesson navigation
- Mobile usability problems
- Weak interaction affordances
- Accessibility barriers
- Cognitive overload

## 3.3 Audit deliverable

Create an internal issue inventory with:

- Problem
- Location
- Severity
- Impact on learning
- Proposed redesign
- Implementation priority

Use this inventory to drive implementation.

Do not stop after producing the audit. Proceed to actual code changes.

---

# 4. DESIGN SYSTEM — CREATE A COMPLETE LEARNING UI LANGUAGE

Establish a cohesive design system before refactoring individual sections.

## 4.1 Color system

Use a carefully controlled educational color palette.

Suggested direction:

- Primary: sophisticated blue / indigo
- Secondary: teal / turquoise
- Success: educational green
- Warning: warm amber
- Error: accessible red
- Surface: white and subtle cool neutrals
- Text: deep slate / charcoal

Colors must have semantic meanings.

Examples:

- Blue: general knowledge and navigation
- Indigo: grammar rules
- Teal: learning activities and examples
- Green: correct answers
- Red: incorrect answers
- Amber: exam tips and important exceptions

Avoid random colors between sections.

Use CSS custom properties as design tokens.

Support consistent backgrounds, surfaces, borders, text, interactive states, and shadows.

## 4.2 Typography

Use modern, legible fonts with excellent Vietnamese and English support.

Possible choices:

- Inter
- Plus Jakarta Sans
- Manrope
- Source Sans 3
- Be Vietnam Pro

Ensure:

- Vietnamese diacritics render correctly.
- IPA characters remain readable.
- Mathematical and grammatical notation remains legible.
- Font sizes work on small screens.

Use a consistent typographic scale.

Establish distinct styles for:

- Application title
- Chapter title
- Lesson title
- Section heading
- Body text
- Example sentence
- Grammar formula
- IPA transcription
- Examination note
- Answer explanation
- Metadata

Avoid tiny instructional text.

## 4.3 Layout system

Use:

- Consistent 8px spacing rhythm
- Controlled content widths
- Responsive grid systems
- Thoughtful whitespace
- Semantic grouping
- Consistent border radii
- Subtle elevation
- Purposeful visual hierarchy

Avoid excessive padding that makes the handbook unnecessarily long.

**Visual density should be optimized for learning, not minimized blindly.**

## 4.4 Component styling

Create reusable styles for:

- Lesson cards
- Grammar rule cards
- Formula blocks
- Example blocks
- Pronunciation cards
- Decision trees
- Timelines
- Comparison tables
- Quiz questions
- Quiz answer choices
- Feedback panels
- Exam-tip callouts
- Summary cards
- Review panels
- Progress indicators

Each component must have a consistent visual and interaction language.

---

# 5. CRITICAL REDESIGN — MERMAID DIAGRAMS AND KNOWLEDGE VISUALIZATION

This is one of the highest-priority parts of the redesign.

The provided screenshots show several serious problems:

1. Large diamond nodes that waste space.
2. Very small text inside diagrams.
3. Excessively long connecting lines.
4. Unbalanced layouts.
5. Large blank areas.
6. Poor visual distinction between questions, conditions, and outcomes.
7. Diagrams that read like technical engineering flowcharts rather than learning tools.

**Do not merely recolor the existing Mermaid diagrams. Rethink how their knowledge should be visualized.**

## 5.1 Choose the best visual representation

For each existing diagram, evaluate whether it should become:

- A redesigned Mermaid flowchart
- A custom HTML/CSS decision tree
- An SVG-based interactive flowchart
- A horizontal grammar timeline
- A step-by-step decision wizard
- An interactive comparison
- A structured rule card
- A compact knowledge map

Choose the representation that best communicates the underlying concept.

Mermaid is not mandatory when a custom accessible HTML/CSS/SVG component would provide a better learning experience.

Do not introduce a heavy framework solely to replace simple diagrams.

## 5.2 Decision trees — pronunciation example

For a diagram explaining how to pronounce the English letter combination "th":

Do not display huge diamond shapes with small text.

Instead, consider a compact educational decision-flow component:

**Start:** Identify the word containing "th".

**Step 1:** Is it a common function word such as "this", "that", "they", or "there"?

- Yes → Typically /ð/ (voiced sound)
- No → Continue to Step 2

**Step 2:** Does the word contain a common "-the" verbal pattern where /ð/ applies, such as "breathe" or "bathe"?

- Yes → /ð/
- No → Continue with the relevant pronunciation rules and exceptions

Use clear visual outcomes:

- /θ/ — voiceless sound
- /ð/ — voiced sound

Include representative examples and audio controls only when genuine playable audio is available.

Important: English pronunciation contains exceptions.

Do not present heuristic rules as universal linguistic truths.

Use educationally appropriate qualifiers and explanations.

## 5.3 Interactive decision-tree requirements

Where practical, support:

- Step highlighting
- Clear Yes/No branching
- Clickable choice paths
- Immediate visual outcomes
- Expandable examples
- Reset / Try again
- Keyboard interaction
- Appropriate mobile stacking

However, do not force every diagram to become interactive.

Static visualizations are acceptable when they are clearer and easier to understand.

## 5.4 Mermaid fallback

When Mermaid remains the optimal choice:

- Use a consistent custom theme.
- Improve node size and text wrapping.
- Reduce unnecessary edge length.
- Increase readable font size.
- Improve branch labeling.
- Remove excessive empty space.
- Use semantic node styles.
- Provide horizontal/vertical layouts appropriate to content.
- Prevent clipping and overlapping.
- Ensure readable fallback on narrow screens.

Avoid fixing layout problems simply by shrinking the diagram.

---

# 6. CRITICAL REDESIGN — GRAMMAR TIMELINES

The current tense timeline uses a dark background and monospace-like presentation.

Although technically informative, its visual style feels disconnected from the surrounding website.

Rebuild grammar timelines as educational visualizations.

## 6.1 Timeline principles

Use a visually meaningful time axis:

**PAST → PRESENT → FUTURE**

Represent grammatical tenses using:

- Clearly positioned temporal markers
- Duration indicators where appropriate
- Event points
- State / result markers
- Distinct labels
- Grammar structures
- Representative examples

For example:

- Past Simple: completed past action
- Present Simple: habits and general truths
- Present Perfect: relationship between past and present
- Future Simple: selected future usages

Do not misrepresent grammar rules to make them fit a simplified timeline.

## 6.2 Visual learning

A student should be able to understand:

- When the tense applies
- How it relates to the present
- Whether the action is completed or ongoing
- The corresponding grammatical structure
- A simple representative example

Consider using compact tense cards beneath the timeline.

## 6.3 Interactions

Where useful:

- Selecting a tense highlights its position.
- Associated formula and example appear.
- Related tenses can be compared.
- Desktop layout supports horizontal temporal reading.
- Mobile layout transforms into a readable stacked representation.

Do not rely solely on colors to distinguish grammatical concepts.

---

# 7. CRITICAL REDESIGN — MULTIPLE-CHOICE EXAM EXPERIENCE

The current MCQ experience resembles:

`1. A. bad | B. man | C. pan | D. bed`

This is insufficient for an engaging, accessible examination practice experience.

**Completely redesign the question-solving interface.**

## 7.1 Question cards

Each question should have:

- Question number
- Clear question stem
- Topic or exercise context when available
- Four distinct selectable answer options
- Appropriate spacing
- Highly visible selected state
- Accessible keyboard interaction

Example structure:

**Question 01 / 10**

Choose the word whose underlined part is pronounced differently.

[A] bad

[B] man

[C] pan

[D] bed

Where letters are underlined in the source, preserve the exact targeted letters.

Do not accidentally remove phonetic emphasis.

## 7.2 Answer behavior

Support two clearly defined learning modes when compatible with existing logic:

**Practice Mode**

- Student selects an answer.
- Student checks the answer.
- The interface displays correctness.
- An explanation appears when available.
- Student may review or retry as permitted.

**Exam Mode**

- Students select answers without immediate correctness feedback.
- A submission action evaluates the completed attempt.
- Final score and answer review become available after submission.
- Unanswered questions are handled explicitly.

Default behavior should respect the original application where appropriate.

Do not reveal correct answers prematurely in Exam Mode.

## 7.3 Answer states

Implement visually distinct states:

- Default
- Hover
- Keyboard focus
- Selected
- Correct
- Incorrect
- Disabled / Submitted

Use icons and textual feedback in addition to color.

Avoid making the correct answer visible before the intended reveal.

## 7.4 Quiz navigation

For larger question sets, provide:

- Question navigator
- Current question indicator
- Answered/unanswered indicators
- Completion progress
- Next/previous controls where useful
- Submit action
- Results summary
- Review incorrect answers

Keep question numbering accurate.

## 7.5 Feedback and explanations

Correct answers should trigger clear, supportive feedback.

Incorrect answers should provide constructive guidance, not merely display a red state.

Where explanations already exist, present them as structured teaching content.

Where explanations are missing:

- Do not fabricate unsupported grammatical explanations.
- Prefer a neutral answer review.
- Add new explanations only when confidently derived and verified.

## 7.6 Progress and gamification

Use subtle motivating elements:

- Progress bar
- Completion percentage
- Answered question counter
- Section completion indicators
- Score summary
- Small success transitions

Avoid:

- Excessive confetti
- Constant popups
- Distracting sound effects
- Meaningless points
- Fake learning statistics
- Overly childish gamification

## 7.7 Underlined pronunciation questions

Pay special attention to questions asking students to identify different pronunciation of underlined letters.

Requirements:

- Preserve precise underlined spans.
- Do not underline entire words incorrectly.
- Ensure underline visibility across desktop and mobile.
- Keep options visually consistent.
- Preserve each question's original answer mapping.

This is a critical educational correctness requirement.

---

# 8. GRAMMAR LESSON COMPONENTS

Avoid presenting grammar lessons as large continuous text blocks.

Transform them into structured learning units.

A typical grammar topic might contain:

1. Concept or title
2. Core grammar formula
3. Usage explanation
4. Recognition indicators
5. English examples
6. Common mistakes
7. Exam tip
8. Quick practice

Do not force empty sections when source content does not provide them.

## 8.1 Formula cards

Grammar formulas such as:

`S + have/has + V3/ed`

should be displayed as distinct educational elements.

Consider:

- Better visual emphasis
- Consistent notation
- Clear positive/negative/question structures
- Compact example alignment
- Readable mobile wrapping

## 8.2 Example blocks

Clearly differentiate English examples from Vietnamese explanations.

Where useful, display:

- English sentence
- Vietnamese interpretation
- Highlighted grammar structure

Do not invent translations when their meaning is uncertain.

## 8.3 Common mistake panels

Use a consistent semantic visual pattern to distinguish:

- Common mistake
- Why it is incorrect
- Correct form
- Short exam-oriented explanation

## 8.4 Comparison layouts

For easily confused grammar structures, prefer comparison interfaces over excessive paragraphs.

Examples:

- Past Simple vs Present Perfect
- Will vs Be going to
- /θ/ vs /ð/
- Different adjective/adverb usages

Maintain accuracy and nuanced distinctions.

---

# 9. LEARNING ARCHITECTURE & NAVIGATION

The application must feel like a structured learning journey.

Consider a coherent application shell with:

## Header

- Application identity
- Current lesson or chapter
- Navigation controls
- Optional learning progress

## Sidebar / Table of Contents

- Chapter navigation
- Section navigation
- Active section highlighting
- Collapsible topic groups
- Completion indicators where genuine state is tracked

## Main learning area

- Clear chapter introduction
- Readable lesson sections
- Relevant visuals
- Practice exercises
- Knowledge recap

## Mobile experience

- Collapsible navigation
- Readable lesson content
- Touch-friendly quiz controls
- No forced desktop layout

## Navigation integrity

- Existing anchors must continue to work or be correctly remapped.
- Deep links should remain usable where practical.
- Sticky elements must not obscure headings.
- Back-to-top and jump-to-section behaviors should remain intuitive.

Do not introduce navigation complexity that exceeds the needs of the application.

---

# 10. LEARNING PSYCHOLOGY

Apply evidence-informed principles of learning design.

## Chunking

Break large knowledge sections into meaningful units.

## Progressive disclosure

Allow students to reveal:

- Additional explanations
- Examples
- Common mistakes
- Advanced notes

Do not hide critical learning information unnecessarily.

## Retrieval practice

Use relevant existing questions to reinforce recently learned concepts.

## Immediate feedback

In practice mode, help students understand mistakes as soon as appropriate.

## Cognitive load management

Avoid presenting multiple competing diagrams, highlights, animations, and dense explanations simultaneously.

## Recognition and comprehension

Make terminology, grammar structures, and pronunciation differences easy to recognize.

## Scannability

Students should be able to locate a relevant rule in seconds without reading an entire chapter.

---

# 11. RESPONSIVE DESIGN REQUIREMENTS

Design for:

- 360px mobile devices
- 390px mobile devices
- 768px tablets
- 1024px laptops
- 1440px desktop monitors
- Large desktop screens

Requirements:

- No unintended horizontal page overflow
- Readable typography at every breakpoint
- Touch-friendly controls
- Responsive tables
- Adaptable diagrams
- Responsive timelines
- Accessible navigation
- Appropriate content width on wide displays

Do not simply shrink desktop components to fit mobile.

Redesign complex visual structures for smaller screens.

---

# 12. ACCESSIBILITY

Target WCAG 2.2 AA principles where reasonably achievable.

Implement:

- Semantic HTML
- Proper heading hierarchy
- Correct button semantics
- Accessible answer selection
- Visible keyboard focus
- Logical tab order
- Accessible labels
- Sufficient color contrast
- Screen-reader-friendly quiz feedback
- Status announcements where appropriate
- Reduced-motion support
- Touch targets suitable for mobile interaction

Do not rely solely on hover interactions.

Do not communicate correctness using only red and green.

---

# 13. MICRO-INTERACTIONS & MOTION

Use purposeful interaction design.

Examples:

- Soft card hover transitions
- Smooth active-tab indicators
- Answer selection animation
- Expand/collapse transitions
- Quiz progress updates
- Correct-answer confirmation
- Chapter navigation highlighting

Animations should feel refined and responsive.

Avoid:

- Continuous movement
- Excessive bounce effects
- Distracting page transitions
- Heavy animation libraries without justification

Support:

`prefers-reduced-motion`

---

# 14. ARCHITECTURE & IMPLEMENTATION CONSTRAINTS

The target is an existing HTML-based application.

Do not automatically migrate it to React, Vue, Next.js, or another framework.

First evaluate whether the current architecture can support the improvements with:

- Semantic HTML
- Modern CSS
- CSS custom properties
- Vanilla JavaScript
- Reusable functions
- Lightweight rendering helpers
- Existing Mermaid integration, where appropriate

## 14.1 Single-file compatibility

If the original application is designed as a standalone HTML file, preserve that deployment model unless there is a compelling technical reason to change it.

Prefer producing an upgraded HTML file that can still be opened directly in a browser.

Do not require a development server merely to view the handbook unless an existing feature genuinely requires one.

## 14.2 Dependencies

Avoid unnecessary external libraries.

If Google Fonts, Mermaid, or other resources require network access, ensure that the application remains usable when those resources are unavailable.

Do not introduce external CDN dependencies without considering offline behavior.

If practical, provide or retain an offline-compatible deployment option.

## 14.3 CSS architecture

Refactor:

- Duplicated selectors
- Conflicting declarations
- Excessive inline styles
- Inconsistent spacing values
- Unused CSS
- Overly specific selectors

Use organized style sections, component classes, and reusable design tokens.

## 14.4 JavaScript architecture

Refactor:

- Duplicated event handlers
- Fragile DOM queries
- Repeated rendering logic
- Unclear quiz state handling
- Mixed content and presentation logic

Use stable event handling and clearly defined application state.

Where applicable, model quiz state explicitly:

- Selected answers
- Answer verification
- Submission state
- Scores
- Question navigation
- Progress state

Avoid accidental answer-key exposure during exam interaction.

## 14.5 Progress persistence

If adding saved learning progress:

- Use localStorage where appropriate.
- Keep data local by default.
- Avoid retaining unnecessary personal information.
- Provide reset behavior.
- Handle invalid or outdated saved state gracefully.
- Do not overwrite or conflict with existing persisted state.

Do not claim cross-device synchronization without a real backend.

---

# 15. VISUAL QUALITY STANDARD

The final result must feel intentionally designed.

Focus on:

- Clear hierarchy
- Consistent component language
- Harmonious palette
- Excellent typography
- Professional spacing
- Information-rich but uncluttered layouts
- Well-integrated diagrams
- Delightful quiz interactions
- Polished navigation
- Careful empty/loading/error states where applicable

Avoid superficial redesign strategies such as:

- Changing only the background color
- Adding border radius to every container
- Applying shadows everywhere
- Replacing every section with the same generic card
- Turning all content into accordions
- Adding gradients without semantic purpose
- Recoloring Mermaid while keeping unreadable geometry
- Increasing whitespace without improving information structure

**The application should look and behave fundamentally better, not merely different.**

---

# 16. REQUIRED IMPLEMENTATION WORKFLOW

Follow this sequence.

## Phase 1 — Inspect

Read the complete HTML source and identify:

- All educational content
- All diagrams
- All question types
- All interactive elements
- All existing scripts
- All external dependencies
- All existing user-facing functionality

## Phase 2 — Architecture and design

Define:

- Design tokens
- Component patterns
- Typography system
- Navigation structure
- Question interaction model
- Diagram rendering strategy
- Responsive behavior
- Accessibility patterns

## Phase 3 — Build foundation

Implement:

- Global design system
- Application layout
- Header and navigation
- Responsive content containers
- Reusable educational components

## Phase 4 — Transform educational content

Refactor each content type using the most suitable component.

Pay special attention to:

1. Pronunciation decision trees
2. Tense timelines
3. Grammar formulas
4. Multiple-choice questions
5. Exam notes and knowledge summaries

Do not leave parts of the handbook visually disconnected from the new system.

## Phase 5 — Implement meaningful interactions

Add appropriate functionality including:

- Interactive answers
- Quiz evaluation
- Practice/exam modes where suitable
- Explanations
- Question navigation
- Progress tracking
- Interactive diagram traversal
- Responsive chapter navigation

Preserve original behavior unless intentionally replaced with an equivalent or better interaction.

## Phase 6 — Test

Perform regression and UI testing.

At minimum validate:

- Original chapters and lessons still exist.
- Original question counts are preserved.
- Question ordering is correct.
- Answer options remain correctly mapped.
- Correct-answer keys are preserved or documented if corrected.
- Underlined pronunciation spans are preserved.
- Diagrams render correctly.
- No diagram text is clipped.
- No JavaScript runtime errors occur.
- Quiz scoring works correctly.
- Practice and exam behavior are correctly separated.
- Keyboard interaction works.
- Mobile layouts are readable.
- Offline behavior remains acceptable.
- Navigation links work.
- Learning progress is accurate.
- Reset/retry operations work as intended.

Use browser-based visual inspection when tooling is available.

Take screenshots at representative viewport sizes and inspect them, especially for diagrams and question cards.

Do not claim browser testing occurred unless it actually did.

## Phase 7 — Polish

Perform a final visual refinement pass.

Look for:

- Inconsistent padding
- Misaligned elements
- Too-small labels
- Low-contrast text
- Awkward line wrapping
- Overflowing diagrams
- Empty-space imbalance
- Poor question spacing
- Inconsistent component treatment

Fix these issues before considering the work complete.

---

# 17. DELIVERABLES

## Primary deliverable

A fully implemented, redesigned version of:

`.\Cam_Nang_On_Thi_Vao_10_Master.html`

The result must be functional code, not a mockup.

## Supporting deliverables

Provide a concise implementation report containing:

### A. UX audit summary

Major problems discovered in the original application.

### B. Design decisions

The visual system and component architecture selected.

### C. Content visualization improvements

Explain how different knowledge structures were redesigned.

### D. MCQ experience improvements

Describe answer selection, correctness feedback, progress, and review behavior.

### E. Content integrity verification

Report:

- Chapters preserved
- Questions preserved
- Answer-key integrity
- Content corrections, if any
- Features preserved

### F. Testing results

Describe tests actually executed and any remaining limitations.

### G. Before/after comparison

Summarize concrete improvements in:

- Readability
- Diagram usability
- Quiz interaction
- Navigation
- Mobile experience
- Accessibility
- Maintainability

---

# 18. ACCEPTANCE CRITERIA

Consider the task complete only when all applicable conditions are satisfied.

**Design**

- The interface has a cohesive, premium educational identity.
- Every major content type uses an appropriate visual representation.
- Diagram styling is substantially better than the original.
- Dense educational information is easier to understand.

**Learning experience**

- Students can navigate lessons efficiently.
- Grammar rules are easy to scan.
- Decision trees are easy to follow.
- Timelines communicate tense relationships clearly.
- Quiz questions are comfortable to answer.
- Feedback supports learning rather than merely indicating correctness.

**Functional integrity**

- No original question is lost.
- No answer mapping is accidentally changed.
- Existing navigation remains usable.
- JavaScript behavior works reliably.
- The file remains usable in its intended runtime environment.

**Responsive and accessible**

- Desktop and mobile layouts are thoughtfully designed.
- No critical information is clipped.
- Keyboard navigation is supported.
- Accessibility and reduced-motion requirements are respected.

**Engineering**

- Code is understandable and maintainable.
- Duplicated styling is substantially reduced.
- UI behavior is organized into reusable structures.
- No unnecessary framework migration is introduced.
- Testing claims are evidence-based.

---

# 19. FINAL QUALITY DIRECTIVE

This is a major product redesign, not a CSS cleanup task.

You have permission to fundamentally reconsider the presentation and interaction of the existing content.

Be ambitious in design, disciplined in implementation, and conservative with educational correctness.

When deciding between two implementations, prioritize:

1. Educational correctness
2. Learning effectiveness
3. Usability and accessibility
4. Visual clarity
5. Performance and maintainability
6. Decorative aesthetics

Do not stop at a proposal, design specification, or isolated sample component.

**Implement the complete redesign directly in the target HTML application.**

Do not ask for approval after each phase unless a genuine blocker prevents safe progress.

Do not deliver only a redesigned sample section while leaving the rest of the handbook unchanged.

The intended outcome is a polished, production-quality English exam-preparation learning experience that students would genuinely enjoy using.

**Transform the experience from "reading an HTML handbook" into "learning through a thoughtfully designed interactive educational application."**