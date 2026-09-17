from pathlib import Path
import json,re,html,math
R=Path(__file__).resolve().parents[1]
S={
'epa':{'name':'U.S. EPA — A Brief Guide to Mold, Moisture and Your Home','url':'https://www.epa.gov/mold/brief-guide-mold-moisture-and-your-home'},
'grade':{'name':'Building America Solution Center — Final Grade Slopes Away from Foundation','url':'https://basc.pnnl.gov/resource-guides/final-grade-slopes-away-foundation'},
'ground':{'name':'Building Science Corporation — Groundwater Control, Info-101','url':'https://buildingscience.com/documents/information-sheets/groundwater-control'},
'basements':{'name':'Building Science Corporation — Understanding Basements, BSD-103','url':'https://buildingscience.com/documents/digests/bsd-103-understanding-basements'},
'cdc':{'name':'CDC — Safety Guidelines: Reentering Your Flooded Home','url':'https://www.cdc.gov/floods/safety/reentering-your-flooded-home-safety.html'},
'french':{'name':'NDS — French Drain Installation Guide','url':'https://www.ndspro.com/us/en/resources/articles/french-drain-installation-guide'},
'channel':{'name':'NDS — 12-inch Pro Series Channel Drains','url':'https://www.ndspro.com/us/en/products/drainage/channel-trench-drains/12-in-pro-series-channel-drains'},
'sump':{'name':'Building America Solution Center — Drains and Sump Pumps','url':'https://basc.pnnl.gov/resource-guides/drain-or-sump-pump-installed-basements-or-crawlspaces'},
'injection':{'name':'Sika — Injection Technologies and Their Applications','url':'https://www.sika.com/en/construction/injections.html'},
'epoxy':{'name':'Sika — Multi-Purpose Epoxies','url':'https://www.sika.com/content/us/main/en/construction/repair-protection/multi-purpose-epoxies.html'},
'slab':{'name':'Building America Solution Center — Capillary Break Beneath Slab','url':'https://basc.pnnl.gov/resource-guides/capillary-break-beneath-slab-polyethylene-sheeting-or-rigid-insulation-over'},
'foundation':{'name':'U.S. DOE / ORNL — Builders Foundation Handbook, Slab Foundations','url':'https://foundationhandbook-qa.ornl.gov/handbook/section4-1.shtml'},
'wet':{'name':'Schluter Systems — Waterproof Shower','url':'https://www.schluter.com/schluter-us/en_US/Waterproof-Shower'},
'water-test':{'name':'Schluter Systems — What Is a Water Test?','url':'https://www.schluter.com/schluter-us/en_US/faq/shower-system-water-test-how-to'},
'kerdi':{'name':'Schluter Systems — KERDI Waterproofing Membrane','url':'https://www.schluter.com/schluter-us/en_US/Membranes/Waterproofing-%28KERDI%29/Schluter-KERDI/p/KERDI'},
'humidity':{'name':'U.S. EPA — Mold Course, Chapter 2: Moisture and Humidity','url':'https://www.epa.gov/mold/mold-course-chapter-2'},
'salts':{'name':'The Concrete Society — Salt Efflorescence','url':'https://www.concrete.org.uk/fingertips/salt-efflorescence/'},
'floor':{'name':'Building America Solution Center — Water Management of Existing Basement Floors','url':'https://basc.pnnl.gov/resource-guides/water-management-existing-basement-floor'},
'fema':{'name':'FEMA / National Flood Insurance Program — Minimize Flood Damage','url':'https://www.floodsmart.gov/prepare/minimize-damage'},
'coating':{'name':'U.S. DOE — Concrete Foundation Walls: Damp-Proofing and Waterproofing','url':'https://bsesc.energy.gov/energy-basics/concrete-foundation-walls-damp-proofed-and-waterproofed'},
}
A=[]
def add(slug,title,category,image,desc,lead,takeaway,body,sources,related_service):
 A.append(dict(slug=slug,title=title,category=category,image=image,description=desc,lead=lead,takeaway=takeaway,body=body.strip(),sources=[S[s] for s in sources],service=related_service))
add('basement-water-after-rain','Water in the basement after rain: what to check first','Basement moisture','hero',
'Water in your basement after rain? Learn how to document the entry point, distinguish runoff from groundwater, and prepare for a waterproofing assessment.',
'The most useful clue is not just that the basement is wet. It is where the water appears, when it arrives, and what is happening outside at the same time.',
'Identify the pattern before choosing a repair. The visible puddle may be several feet from the actual entry point.',
'''
## Start with safety, not the puddle
Do not step into standing water near wiring, appliances, or electrical equipment. The CDC warns against operating electrical switches or tools while standing in water. If reaching the electrical shutoff requires entering water, have a qualified professional handle it. Suspected sewage, gas, rapid flooding, or structural instability calls for the appropriate emergency or utility response—not a routine online inquiry. [1]

Once the area is safe to observe, resist the urge to label every rain-related leak a foundation failure. An observation is more useful than a guess: “water appears at the rear floor edge two hours after rain” gives an assessor a starting point. “The whole foundation needs replacing” jumps past the evidence.

## Follow the water from outside to inside
Surface runoff and groundwater are related, but they are not identical. A driveway can send water toward a door while saturated soil creates pressure below grade. Building Science Corporation separates surface drainage, below-grade drainage, and control of moisture moving through porous materials because each addresses a different part of the problem. [2]

From a safe, accessible position, note overflowing gutters, downspouts ending near walls, pooled water beside patios, or soil that appears to fall toward the home. Do not climb a roof or enter an excavation to collect evidence. A short video taken from a window can be more useful than a risky close-up.

Treat the observations as a map. Mark the wet interior area on a simple floor plan, then label the corresponding exterior wall. Add doors, window wells, downspouts, retaining walls, and hardscapes. This makes a complicated house easier to discuss without knowing construction terminology.

## Record the timing of the leak
Keep a short event log: date, approximate start of rain, when you noticed moisture, where it appeared, and whether any existing pump was operating. Note whether the room dries between events or stays damp. Do not rely on a memory of the single worst storm.

For example, compare two hypothetical observations. Water flowing under an exterior door during a downpour suggests a different investigation from water emerging along the slab edge after a prolonged wet period. Neither observation proves a diagnosis. Both help direct the next questions.

Include changes you made recently. A new patio, relocated downspout, landscaping work, or basement finishing project may be relevant context. A clear timeline helps an assessor decide what to examine first; it does not mean the most recent contractor necessarily caused the leak.

## Understand what a proposed repair is supposed to do
Ask the contractor to explain the route of the water and the function of every proposed element. Is the plan intercepting surface runoff, draining water near the footing, sealing a specific opening, or adding protection to the exterior wall? Several approaches may be combined.

The Building America Solution Center emphasizes grading and drainage that move water away from the foundation, including alternatives where a site's geometry limits grading. That is a reason to examine the whole perimeter rather than treating the indoor stain in isolation. [3]

A dehumidifier can be useful for humidity, but it is not a substitute for explaining a stream of incoming water. Likewise, a fresh painted surface is not evidence that the source has been resolved. Ask how the completed work will be checked, what remains outside scope, and what maintenance you will be responsible for.

## Bring a useful evidence pack
Prepare wide photos of the room and close photos of the affected surface. Include a sketch of the location, the event log, known previous repairs, and any available plans. Take photos before covering or repainting a stain. Only move belongings when it is safe to do so.

Ask for an explanation you can repeat in one sentence: “This system collects water at this location and carries it to that discharge point.” If the explanation stays vague, request a drawing or written clarification before comparing prices.

## Your next step
Start with our [foundation leak service](/services/foundation-leaks/) when water is appearing around below-grade walls. The [French drain versus trench drain guide](/blog/french-drain-vs-trench-drain/) explains two frequently confused drainage approaches. You do not need to select a system before speaking with the team. Bring the pattern; let the assessment establish the scope.
''',['cdc','ground','grade'],'foundation'),
add('exterior-vs-interior-waterproofing','Exterior vs. interior basement waterproofing: compare the jobs, not just the price','Foundations','foundation',
'Compare exterior waterproofing and interior drainage by purpose, access, disruption, discharge, and maintenance before choosing a basement repair approach.',
'Two proposals can both say “basement waterproofing” while doing very different work. A useful comparison starts with the problem each proposal intends to solve.',
'Exterior barriers and interior collection systems are not interchangeable. Compare the water path, access, scope, and long-term responsibilities.',
'''
## Define the objective first
“Waterproofing” is sometimes used as a broad label for work that keeps a room usable. Be more specific when reviewing a proposal. Does it resist water at the exterior wall? Does it collect incoming water and route it out? Is the aim to control moisture vapor, repair a discrete opening, or combine these measures?

Building Science Corporation distinguishes liquid water, capillary movement, and vapor behavior in basements. A plan focused on one mechanism should not automatically be assumed to address all three. [1] Your first question is therefore simple: which mechanism has the assessment identified, and which parts of the proposed work address it?

## What exterior work may involve
Exterior foundation protection concerns the outside of the below-grade wall and its connections to surrounding details. Depending on the assessment, the scope may involve surface preparation, a specified membrane or coating, drainage layers, protection before backfill, and attention to penetrations or transitions. DOE guidance describes exterior foundation treatments as part of a broader water-management approach, not an isolated finishing coat. [2]

Access is a major planning question. Walkways, planted areas, property boundaries, utilities, and structures next to the wall may affect feasibility. Ask who is responsible for investigating these constraints and what restoration is included. A quote that excludes replacing a patio is not directly comparable with one that includes it.

Do not treat “exterior” as an automatic promise that no water can ever enter. Ask exactly which walls, depths, joints, and adjacent conditions are covered. The detail at the end of a membrane matters just as much to the discussion as the name printed on its packaging.

## What interior work may involve
Interior approaches may include drainage channels, collection at the perimeter, a wall drainage layer, or a sump system. A foundation drain and pump manage collected water by providing a route to a suitable discharge. The Building America Solution Center notes that pumping water back beside the foundation can create a recurring collection loop. [3]

A system designed to manage water inside the perimeter does not necessarily stop the exterior wall from getting wet. Ask what the plan means for the existing wall, finished materials, humidity control, and future access. This distinction is especially important before building a new finished wall in front of the original foundation.

Interior access also has costs: protecting belongings, opening floor edges, removing finishes, and restoring surfaces. Have those items described clearly. Ask where equipment and access panels will sit after the project is finished rather than discovering them when furniture is moved back.

## Compare five things in every proposal
**Cause and evidence:** What was observed, what remains uncertain, and what additional assessment is needed? A quote should not turn an unverified assumption into a guaranteed diagnosis.

**Physical scope:** Ask for the actual locations, lengths or areas, transitions, and exclusions. “Complete waterproofing” is difficult to evaluate without a drawing or schedule of work.

**Discharge and power:** Where will collected water go? Who confirms local discharge requirements? If pumping is proposed, what happens during a power interruption, and what backup or alarm options are being discussed?

**Restoration and maintenance:** Identify who restores landscaping or interior finishes, who checks equipment, and what must remain accessible. Maintenance commitments should not be left to inference.

**Written terms:** Compare the specific coverage, exclusions, transfer conditions, and maintenance requirements of any offered warranty. Do not assume two differently worded promises mean the same thing.

## A hypothetical comparison
Imagine one proposal seals a single identified crack, while another installs perimeter drainage. The cheaper number does not tell you which is more suitable because the scopes differ. Ask each bidder what evidence supports treating the problem as localized or broader, and what result the proposed scope is designed to achieve.

This same discipline applies to exterior versus interior work. Clarifying the job often resolves more confusion than comparing brands or asking which approach is always best. There is no substitute for evaluating your actual building and site.

## Plan before you finish the room
Keep waterproofing decisions ahead of expensive finishes when possible. Use our [foundation leak page](/services/foundation-leaks/) and [consultation checklist](/blog/waterproofing-consultation-checklist/) to prepare the conversation. The goal is a documented plan you understand—not a label that simply sounds more comprehensive.
''',['basements','coating','sump'],'foundation')
add('french-drain-vs-trench-drain','French drain vs. trench drain: which water are you trying to move?','Drainage','drainage',
'French drains and trench drains collect water differently. Understand surface runoff, subsurface collection, outlets, and questions to ask before installation.',
'A drainage system is a route: water enters, moves through it, and leaves somewhere appropriate. The right starting point is understanding that route.',
'French drains typically collect along a permeable subsurface path. Grated trench or channel drains intercept surface runoff. Terminology can vary—ask to see the detail.',
'''
## The practical difference
A conventional French drain uses a permeable collection zone, often with aggregate and perforated pipe, to collect water along its length. It can address subsurface water and, depending on the arrangement, surface water entering through the collection zone. NDS describes this distributed collection as distinct from capturing water at a single point. [1]

A grated trench or channel drain is typically a linear surface collector. Its visible grate intercepts runoff crossing a driveway, patio, walkway, or similar hardscape and routes it into connected drainage. NDS identifies hardscape surface-water collection as an application for its channel drains. [2]

Contractors and homeowners sometimes use these terms differently. Rather than debating the name, ask to see a cross-section: what is open at the surface, what is perforated below it, and where does the collected water leave? That drawing is more useful than a category label.

## Match the conversation to the observation
Describe the problem in ordinary language. Is water running across paving toward a garage opening? Is a planting bed staying saturated beside a foundation? Is moisture appearing below grade? Those observations frame different drainage questions without requiring you to specify a system.

A hypothetical driveway with visible runoff at a threshold may prompt a surface-interception discussion. A persistently saturated strip of soil may prompt investigation of subsurface collection. The examples illustrate the difference; they are not a diagnosis of every property with similar symptoms.

A plan can also use more than one collection method. What matters is whether the elements connect into a coherent route and whether the assessment supports each one. More drains do not automatically mean a better design.

## The outlet is not an afterthought
Ask where water will go before discussing the appearance of a grate. Is the outlet accessible? Is it lower than the collection point, or is a pump needed? Who evaluates the site's soils and the suitability of infiltration? Who confirms the applicable local requirements and avoids discharging onto neighboring property?

For foundation drainage, the Building America Solution Center describes discharge away from the building and warns against putting pumped water back next to the foundation. [3] A collection system with an unsuitable destination does not complete the water-management task.

Document any existing buried system if plans are available. “Connect to the old drain” should come with an explanation of how that drain's location, condition, and destination will be confirmed. Unknown infrastructure is a question to investigate, not an assumption to hide inside a quote.

## Ask about access and maintenance
Clarify how the proposed system will be inspected and cleaned. Surface grates may need accessible debris removal, while buried systems may need appropriately located access points. NDS notes removable grates as a maintenance feature of its channel-drain system. [2] The specific inspection routine should come from the installed system's requirements.

Ask what landscaping or paving can be placed over or near the system and what must remain reachable. Have the final route recorded before it is concealed. A few labeled handover photos can save confusion when a future landscaping or renovation project begins.

Also ask who handles utility checks, excavation planning, restoration, and protection of adjacent structures. This guide is a planning resource, not an instruction to dig beside a footing yourself.

## Compare proposals with the same checklist
Write down the collection method, proposed route, discharge destination, access points, restoration, and maintenance. Request clarification when one proposal includes these details and another supplies only a total length and price.

There is no universal price or depth in this article because those numbers depend on the actual project. A generic online dimension should not replace the drainage plan for your home. The most useful quote makes its assumptions visible.

## Start with the water path
Our [French and trench drain services](/services/drainage-systems/) bring the two approaches into one conversation. For rain-related basement concerns, also read [what to check after rain](/blog/basement-water-after-rain/). Bring a video of the water path taken safely during an event, plus a sketch of where you believe existing drains lead.
''',['french','channel','sump'],'drainage')
add('foundation-crack-injection','Foundation crack injection: stopping a leak is not the same as repairing structure','Foundations','cracks',
'Understand the difference between leak-sealing and structural crack repair, what epoxy and polyurethane can do, and what to document before an assessment.',
'A crack may be a water pathway, a sign of movement, or both. A sound repair discussion separates those questions instead of treating every opening alike.',
'Ask what caused the crack and what the proposed repair is designed to achieve. A dry surface alone does not establish structural adequacy.',
'''
## Separate two very different objectives
One objective is reducing water passage through an opening. Another is restoring or addressing structural performance. These objectives can overlap, but they are not automatically satisfied by the same material or method.

Sika's injection guidance distinguishes rigid materials used for applications such as structural repair from flexible materials used for water-stopping applications. Its broader epoxy guidance also notes the role of movement and leakage in choosing an injection approach. [1][2] That is why a request for “crack injection” should begin with assessment, not a product selected from a photo.

A homeowner's useful question is: “Are you proposing a leak seal, a structural repair, or a combination—and what supports that choice?” This does not require technical expertise. It requires the scope to be explained plainly.

## What to record before the visit
Photograph the entire wall and the opening in context. A close-up without surroundings can be misleading. Include corners, openings, adjoining surfaces, and the floor edge when it is safe and practical to do so.

Record when you first noticed the crack, whether it has visibly changed, whether moisture appears nearby, and whether anyone has previously sealed or covered it. Save available repair invoices and older photos. Do not conceal the area just to make it look better before an assessment.

If measurements are practical without risk, include a scale in the photograph, but do not use a single measurement to declare a crack harmless. An assessor may need to evaluate its pattern, depth, movement history, material, loading context, and adjacent conditions.

## Why material names do not settle the question
“Epoxy” and “polyurethane” describe families of products, not universal repair instructions. Suitability depends on the specific product, the condition being treated, and the preparation and installation requirements. A product's marketing category is not enough information to select it for a particular wall. [1][2]

Ask for the exact product or system intended for your project, the repair objective, and any limitations the installer expects. Ask how the plan accounts for a crack that is wet or may continue to move. This guide does not provide injection pressures, mixing ratios, or installation steps because those belong to the assessed repair and the manufacturer's instructions.

Be cautious about promises that every visible crack can be solved identically. A clear explanation of uncertainty is more useful than a blanket assurance that one material handles everything.

## Look beyond the opening
Even when a crack is the visible entry point, the surrounding water conditions remain relevant. Ask whether runoff, grading, and drainage are also being evaluated. Repairing one path and addressing the water pressure around the wall are different parts of the same investigation.

The Building America Solution Center describes exterior grading and drainage as ways to limit water saturation near foundations. [3] That does not establish the cause of your crack, but it supports looking at the property around the wall rather than only at the line on its surface.

For example, a recurring leak following heavy rain may justify asking how the proposed repair relates to exterior water conditions. A crack appearing in a new addition may call for different questions about the building and construction history. These are discussion prompts, not diagnostic rules.

## Know when to escalate the assessment
Ask for evaluation by an appropriately qualified structural professional when there is concern about movement, displacement, bowing, or stability. Do not interpret this article or the site's visual model as a structural assessment. If part of the building appears unstable, keep people away and use the appropriate urgent professional or emergency channel.

A waterproofing proposal should be able to identify what it does not cover. If structural evaluation is outside the contractor's scope, document who will address it and how that work affects the proposed water repair.

## Request a clear handover
Keep the assessed scope, materials, photographs, written terms, and any monitoring instructions. Ask how the repair will be checked and what should prompt another call. A useful handover lets you distinguish a completed task from a broader issue that still needs attention.

Use our [crack injection service page](/services/crack-injections/) to start the conversation. Bring your observations and history; do not feel you need to arrive with a repair method already chosen.
''',['injection','epoxy','grade'],'cracks')
add('underslab-waterproofing-planning','Underslab waterproofing: the decisions to make before the concrete arrives','New construction','underslab',
'Plan underslab moisture protection before a pour: distinguish vapor barriers from waterproofing, coordinate penetrations, and document concealed details.',
'Once a slab is poured, the layers beneath it are difficult to revisit. The best time to clarify them is while the design, access, and sequence can still change.',
'Vapor control, capillary breaks, and hydrostatic waterproofing have different jobs. Specify the required performance before choosing a membrane.',
'''
## Start with the performance required
A slab can interact with ground moisture in more than one way. A capillary break interrupts liquid moisture movement through connected pores. A vapor-retarding layer limits moisture vapor movement. A waterproofing assembly may need to address liquid water under pressure. Do not assume one label establishes performance against every mechanism.

The Building America Solution Center discusses capillary-break materials, continuous sheeting, sealed seams, and penetrations as parts of slab moisture control. The DOE foundation handbook also distinguishes slab-on-grade moisture layers from situations requiring traditional waterproofing. [1][2] The design professional should establish what your site and building require.

Before requesting a quote, ask a useful first question: “Which moisture conditions is this assembly designed to resist?” The answer should be specific enough to guide product selection and detailing rather than simply saying “we put plastic underneath.”

## Coordinate the details before the pour
Make a list of penetrations, columns, pits, changes in level, and connections to walls. Identify which trades introduce those details and who owns their treatment. A continuous field membrane can be interrupted by a pipe or last-minute alteration; coordination is part of preserving the design intent.

Create a simple decision log. Each unresolved detail gets an owner, a drawing reference if available, and a deadline before it is covered. For a small residential project, this can be a one-page checklist rather than an elaborate project-management system.

If plans change, ask for the waterproofing detail to be revisited explicitly. The plumbing revision and the membrane detail should not become two separate conversations that never meet.

## Agree on the construction sequence
Discuss when the substrate will be ready, when the moisture-protection layers are installed, how they are protected from traffic, and who checks them before concealment. Do not treat the concrete arrival time as the only deadline that matters.

Ask how damage or unfinished work will be handled if it is found before the pour. A written hold point—an agreed check before proceeding—can make responsibilities much clearer. It is a coordination suggestion, not a substitute for required inspections or the manufacturer's installation procedure.

The precise assembly, thickness, lap requirements, cure conditions, and inspection criteria belong to the project's documents and the specified system. This homeowner guide intentionally avoids presenting a universal construction detail.

## Document what will disappear
Request photographs that show completed details in relation to identifiable features of the building. A close-up of a membrane without a location is hard to interpret later. Label the images by area, date, and drawing reference where available.

Keep the product documentation, installer information, inspection records, and any approved changes together. Ask for the final record before the project team disperses. This is particularly useful when a later renovation adds plumbing or alters the floor.

For example, an owner planning a future kitchen in the basement should discuss that intention while penetrations and service routes can still be coordinated. The point is not to predict every future change; it is to avoid known plans being omitted from today's details.

## Keep the surrounding water plan in view
Underslab protection belongs to a wider foundation strategy. Building Science Corporation describes keeping rainwater away from the foundation perimeter and managing groundwater through suitable drainage as separate, complementary tasks. [3]

Ask how the below-slab layers connect to wall protection and drainage where applicable. A proposal that describes only the middle of the slab may leave the important edge details unresolved. Ask about those transitions instead of judging the plan only by the membrane brand.

## Questions for your project team
Before work is concealed, confirm the intended performance, current drawings, treatment of penetrations, responsible installer, protection during construction, pre-cover inspection, and handover records. Identify any exclusions. Do not approve a pour based on an article or a visual model.

Our [underslab and waterproofing wraps service](/services/underslab-waterproofing/) and [concrete foundation service](/services/concrete-foundations/) are starting points for coordinating the discussion. Bring the current plans and construction schedule so the assessment can address the actual project.
''',['slab','foundation','ground'],'underslab')
add('shower-waterproofing-beneath-tile','Shower waterproofing: what needs to work before the tile looks beautiful','Wet areas','wetarea',
'Tile is the finish, not the waterproofing plan. Understand shower membranes, transitions, drains, water testing, and the questions to ask before installation.',
'A beautiful tile installation is the visible result. A connected water-management assembly underneath is what the waterproofing conversation needs to address.',
'Ask about the complete assembly—floor, walls, corners, openings, and drain—not just the tile or grout.',
'''
## Tile and grout are not the waterproofing system
Schluter states that tile and grout are not inherently waterproof. The underlying assembly must manage water rather than relying on the decorative finish alone. [1] This distinction matters when a shower looks immaculate but moisture is reaching adjoining materials.

Ask the team to describe the waterproofing system before discussing grout colors. Which parts provide water protection? How do they connect? What is the intended substrate? Who checks the concealed work? These questions do not make a project less design-focused. They protect the investment in the finished design.

A new bead of surface sealant may be appropriate maintenance in some circumstances, but it should not automatically be treated as a diagnosis or complete repair of a leaking shower. Have the cause and the intended scope assessed.

## Think in connections, not isolated products
The floor-to-wall junction, corners, drain connection, curb or entrance, niches, benches, and pipe penetrations all deserve explicit coordination. Ask how the specified system handles each detail. A collection of individually water-resistant products is not automatically a complete waterproof assembly.

Manufacturer instructions matter. For example, Schluter's KERDI guidance addresses seams, corners, connections, movement joints, and suitable applications within that system. [2] That is an example of system-specific requirements, not an endorsement of a product for every project or a claim that Waterproofing360 installs a particular brand.

Avoid mixing components simply because they appear compatible. Ask the installer or design professional to identify the documented assembly and explain the basis for combining materials when a mixed system is proposed.

## Plan the details that change the room
A curbless entrance, large niche, built-in bench, linear drain, or window may affect the waterproofing discussion. Bring those design decisions forward rather than leaving them until the surface layout is finalized.

For a renovation, ask what can be assessed without opening finishes and what remains unknown until demolition. A realistic proposal can identify both. It is better to understand an investigation allowance than to discover that an essential detail was assumed to be sound.

A useful design meeting ends with a small drawing showing the proposed assembly, its transitions, and the responsibilities of the trades involved. The purpose is not to make the homeowner the installer. It is to make sure the same room is being imagined by everyone.

## Make room for a water test
Schluter describes water testing before tile installation as a quality-control check. The procedure and waiting time depend on the system and conditions. Its KERDI guidance, for example, describes a wait before testing and a typical test duration; these are separate periods. [3]

Do not apply one product's timetable to every membrane. Ask the installer which instructions govern the work, when testing can begin, what is recorded, and what happens if a leak is found. The project should also address any applicable inspection requirements through the appropriate professional.

Ask for the test record and relevant photos to be included in the handover. The value is in verifying the concealed assembly before it is covered—not in ticking a box after the tile has already been installed.

## Showers, steam rooms, and pools are not interchangeable
Schluter lists specific applications for its membrane and directs users to system guidance for showers and steam environments. [2] A continuously immersed pool, a spa, or a different specialty space requires its own suitability assessment; this shower article is not a pool specification.

Describe the intended use, water exposure, heat or steam conditions, and project constraints early. The finish may look similar across two rooms, while the performance demands and required details differ.

## Protect the finish by planning beneath it
Before installation, clarify the assembly, transitions, responsibilities, documentation, and test plan. Before handover, ask about maintenance and any restrictions on later drilling or modifications. Keep the records with the property's other construction information.

Our [specialty wet-area service](/services/wet-area-waterproofing/) covers conversations about showers, spas, mikvahs, and pools. Bring the design and intended use so the appropriate scope can be discussed before the visible finishes take over the schedule.
''',['wet','kerdi','water-test'],'wetareas')
add('basement-condensation-vs-leaks','Basement condensation or a leak? Read the moisture clues carefully','Basement moisture','concrete',
'Condensation, seepage, and humidity can look similar in a basement. Learn which observations help separate them and when more assessment is needed.',
'A wet pipe, a damp wall, and a puddle at the floor edge can involve different moisture mechanisms. A useful investigation allows for more than one cause.',
'Look at the surface, timing, location, and humidity together. A dehumidifier reading or a single photo cannot explain every moisture problem.',
'''
## The mechanisms can overlap
Condensation occurs when moisture in the air collects on a sufficiently cold surface. Liquid intrusion involves water entering through or around part of the building. A basement can experience both, so identifying condensation on one pipe does not establish that every wet area has the same cause.

EPA's moisture guidance discusses condensation on cold surfaces and the role of indoor humidity. [1] The practical response is to record more than one clue. What is wet? Is the moisture on the room-facing surface? Does it track rain, a plumbing fixture, or a period of humid weather? What do nearby surfaces look like?

Use these observations to guide an assessment, not to run an improvised diagnostic test that could damage finishes or conceal a problem.

## Look at the pattern over time
A useful record is small and repeatable: date, location, weather context, visible condition, and any changes in room use or equipment. Include whether the area is wet continuously or only under particular conditions.

A hypothetical cold pipe that beads with moisture on humid afternoons suggests a different line of investigation from a floor edge that becomes wet after long rain. But either location may still need a closer inspection. The comparison helps organize the questions; it does not establish the final cause.

If you use a humidity meter, record its location and readings rather than treating one number as a verdict. Equipment placement and changing conditions can affect what a snapshot tells you. Ask a qualified assessor how the readings fit the observed materials and water paths.

## What a musty smell can—and cannot—tell you
A recurring musty smell is a reason to investigate moisture. It does not identify a species, quantify an exposure, or prove whether the source is condensation, seepage, or a hidden plumbing leak. Avoid making health or remediation decisions from odor alone.

EPA emphasizes moisture control as central to mold prevention and recommends keeping indoor relative humidity below 60 percent, ideally around 30–50 percent when possible. It also advises prompt attention to wet materials. [2] Those are general moisture-control principles, not a promise that a particular basement problem is solved when a meter reaches a target.

For extensive mold, contaminated floodwater, or health concerns, seek the appropriate qualified professional. Waterproofing and remediation scopes should be discussed separately rather than presumed to be interchangeable.

## Read white deposits with care
White surface deposits on masonry can be efflorescence. The Concrete Society describes salt deposits associated with wetting and drying cycles that bring soluble salts to the surface. [3] That history is useful, but a white deposit is not by itself a complete diagnosis of today's water source.

Photograph the location and note whether it recurs. Include surrounding stains, coatings, cracks, and floor edges in the record. Do not assume every white mark is the same material, and do not select a chemical cleaning method before the surface and cause are understood.

Cleaning a surface and controlling the moisture are different tasks. Ask the assessor how each is addressed in the proposed scope.

## Do not cover the evidence too early
Before installing new flooring or wall finishes, resolve what is known and unknown about the moisture conditions. A refreshed appearance can make future observation harder without changing the underlying mechanism.

Ask what preparation, drying, testing, or further investigation is needed for the intended finishes. Discuss the floor and wall assemblies together. A finish manufacturer's moisture requirements and the building's waterproofing plan answer different questions and both may matter.

The next step should be specific: an inspection, monitoring plan, plumbing check, or water-management assessment—not simply a shopping list of coatings or equipment.

## Build a better first conversation
Bring wide and close photographs, your observation log, available humidity readings, and details of previous work. Explain which rooms are affected and what you intend to do with them. A guest room renovation may raise different planning questions from unfinished storage, even if the visible stain is similar.

Read [water in the basement after rain](/blog/basement-water-after-rain/) for rain-linked patterns, or use the [consultation checklist](/blog/waterproofing-consultation-checklist/) to organize your notes. The objective is to separate the clues clearly enough that the next assessment can address the actual problem.
''',['humidity','epa','salts'],'foundation')
add('waterproofing-consultation-checklist','Your waterproofing consultation checklist: arrive with context, leave with clarity','Planning','evening',
'Prepare for a waterproofing assessment with a practical checklist for observations, plans, scope, discharge, restoration, maintenance, and written terms.',
'You should not need to become a waterproofing specialist to ask good questions. The goal is a first conversation that turns an unclear concern into a documented next step.',
'Bring the property story, not a preselected product. Leave with an explanation of the proposed scope, exclusions, and next decisions.',
'''
## Before the conversation: make a one-page brief
Write down the property location, whether this is an existing concern or planned construction, the affected area, and the outcome you want. “Use the basement for storage without recurring water” is a clearer goal than “make it perfect.” For a new build, include the current construction stage and upcoming milestones.

Add what you know and label what you do not. Perhaps a previous owner mentioned a drain, but you have no plan or outlet location. That is useful context as long as it is presented as unverified. An honest unknown is better than an assumption repeated until it sounds certain.

Your brief can be a note on your phone. Its purpose is to keep the important facts in the conversation, not to create homework for its own sake.

## Collect evidence without taking risks
Use wide photos to show location and close photos to show the concern. A short event log helps explain when moisture appears. Include any available plans, invoices, and records of previous repairs.

Do not enter standing water to retrieve a photograph or operate electrical equipment. CDC guidance warns against electrical operations while standing in water and calls for professional help when a shutoff cannot be reached safely. [1] Safety takes priority over documentation.

Keep original files rather than relying only on annotated copies. A marked-up sketch is helpful, but an assessor may also want the unobstructed photograph. Label the room or exterior elevation in a way that another person can understand.

## Ask for the working explanation
Use direct questions: Where is the water believed to enter? What evidence supports that view? What is still uncertain? Does the concern require additional investigation or another professional's input?

Ask the team to separate a confirmed observation from an assumption. This is especially useful when an assessment is limited by finished walls, buried drains, or inaccessible areas. A proposal can be well organized without claiming to see through every concealed surface.

If more than one mechanism is possible, ask what would distinguish them. You do not need an instant answer to every question, but you do need a clear plan for resolving the questions that affect scope.

## Make the scope visible
Request locations, boundaries, and an explanation of how the proposed elements work together. If drainage is included, ask where the water is collected and where it is discharged. Building America guidance treats foundation drainage and its discharge as linked parts of water management. [2]

If membrane work is proposed, ask how the plan connects to edges, penetrations, and adjacent assemblies. If a targeted repair is proposed, ask which concern it addresses and what broader conditions remain outside the work.

A simple annotated drawing can make two quotes easier to compare. A higher number may include restoration, access work, or a different scope; a lower number may omit them. Ask before treating price alone as the answer.

## Discuss the practical parts of the project
Clarify protection of occupied areas, access routes, storage of materials, work hours, and coordination with other trades. Ask what needs to be moved and who will move it. For new construction, identify the date after which a detail will be concealed or harder to change.

Discuss restoration explicitly. Who repairs paving, replaces planting, patches interior surfaces, or reinstates finishes? Which of those tasks are included, optional, or excluded? Have the answer written into the scope rather than left in a conversation.

Ask how any changes discovered during work will be communicated and authorized. This is a suggested project-control practice, not legal advice about a particular contract.

## Prepare for ownership after installation
Ask what access must remain clear, what equipment needs checking, what documents you will receive, and what should prompt a service call. Request product information and the specific written terms of any offered warranty.

For flood preparedness, FEMA's National Flood Insurance Program highlights measures such as maintained gutters, working sump equipment, water alarms, and protecting belongings when conditions allow. [3] Those ideas belong in a broader property plan; no single installation should be presented as removing every flood risk.

Maintain the handover record with the property's drawings and repair history. The next person working on the building should not have to guess where concealed protection was installed.

## Use the guide, then speak to a person
Our interactive property guide organizes the concern, project type, and location without collecting contact information. It does not diagnose the cause, quote a price, or book an appointment. Copy its summary and bring it into your conversation with [Waterproofing360](/contact/).

A successful first consultation leaves you knowing what happens next, who is responsible for it, and which questions still need answers. That clarity is the starting point for a better project.
''',['cdc','sump','fema'],'foundation')
# Real written content + pre-rendered sections for a stdlib-only website build.
def inline(t):
 t=html.escape(t,quote=False)
 t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
 t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:'<a href="'+html.escape(m[2],quote=True)+'"'+(' data-route="'+m[2]+'"' if m[2].startswith('/') else '')+'>'+m[1]+'</a>',t)
 t=re.sub(r'\[(\d+)\]',lambda m:f'<sup><a href="#source-{m[1]}" aria-label="Source {m[1]}">[{m[1]}]</a></sup>',t)
 return t
for a in A:
 sections=[]
 for part in re.split(r'^## ',a['body'],flags=re.M):
  if not part.strip():continue
  heading,_,text=part.partition('\n'); sid=re.sub('[^a-z0-9]+','-',heading.lower()).strip('-')
  paras=['<p>'+inline(p.replace('\n',' ').strip())+'</p>' for p in text.strip().split('\n\n') if p.strip()]
  sections.append({'id':sid,'title':heading,'html':'\n'.join(paras)})
 a['sections']=sections
 a['words']=len(re.findall(r"\b[\w’-]+\b",a['body']+' '+a['lead']));a['minutes']=max(3,math.ceil(a['words']/210))
 a['date']='2026-09-17'
 (R/'content'/f'{a["slug"]}.md').write_text('# '+a['title']+'\n\n'+a['lead']+'\n\n'+a['body']+'\n\n## Sources\n'+'\n'.join(f'{i+1}. {s["name"]}: {s["url"]}' for i,s in enumerate(a['sources'])))
(R/'content/articles.json').write_text(json.dumps(A,ensure_ascii=False,indent=2))
(R/'content/sources.json').write_text(json.dumps(S,indent=2))
print([(a['slug'],a['words']) for a in A]);print('TOTAL WORDS',sum(a['words'] for a in A))
