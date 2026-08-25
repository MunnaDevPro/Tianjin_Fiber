import os
import django
from django.core.files import File
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from products.models import Category, Product, ProductImage

# ============================================================
# 70 HARDWARE PRODUCTS - Tianjin Tipei Hardware
# ============================================================

HARDWARE_PRODUCTS_70 = [
    # ─── TELESCOPIC / EXTENSION LADDERS (1–10) ───────────────
    {
        "name": "Heavy-Duty Aluminium Telescopic Extension Ladder 1",
        "desc": "<p>Our <strong>Heavy-Duty Aluminium Telescopic Extension Ladder</strong> is manufactured from premium aerospace-grade aluminum alloy, delivering an exceptional strength-to-weight ratio. Designed for professional contractors, maintenance crews, and serious DIY enthusiasts, this ladder telescopes smoothly to reach heights up to 4–7 meters while folding down to a compact, portable form. Each rung is precisely machined with anti-slip serrated grooves, and the locking mechanism engages with a confident click to prevent accidental collapse.</p>",
        "features": "Aerospace-grade 6061-T6 aluminum alloy construction\nNon-slip D-shaped rungs with anti-skid serrated surface\nOne-touch push-button telescopic locking mechanism\nWide outrigger feet with non-slip rubber base pads\nCompact folded length for easy transport and storage\nMaximum load capacity: 150 kg (330 lbs)\nComplies with EN131 and ANSI safety standards"
    },
    {
        "name": "Heavy-Duty Aluminium Telescopic Extension Ladder 2",
        "desc": "<p>The <strong>Telescopic Extension Ladder Series 2</strong> features our upgraded dual-locking rung system for added security at height. Built from 6061-T6 aerospace aluminum with an anodized finish, it extends effortlessly to 5 meters while packing down to just 85cm for storage. Ideal for roofing, painting, and electrical installation work on two-storey properties.</p>",
        "features": "Upgraded dual-locking rung system for extra security\nAnodized 6061-T6 aluminum for corrosion resistance\nExtends to 5 meters, packs to 85cm\nExtra-wide anti-slip step rungs\nOverride safety lock prevents accidental retraction\nMaximum load: 150 kg\nCarrying bag included"
    },
    {
        "name": "Heavy-Duty Aluminium Telescopic Extension Ladder 3",
        "desc": "<p>Our <strong>Series 3 Telescopic Extension Ladder</strong> is engineered for heavy commercial use. The thicker wall aluminum extrusion provides enhanced rigidity under maximum load, while the precision-machined locking buttons deliver positive engagement at every rung position. The textured black rubber feet are oversized for stability on wet and uneven ground.</p>",
        "features": "Thick-wall aluminum extrusion for enhanced rigidity\nPrecision-machined spring-loaded locking buttons\nOversized textured rubber feet for wet/uneven surfaces\nExtends to 6 meters, collapses to 97cm\nRated for continuous professional use\nMaximum load: 150 kg\nEN131 certified"
    },
    {
        "name": "Aluminium Single-Section Extension Ladder 4",
        "desc": "<p>The <strong>Single-Section Extension Ladder</strong> provides a straightforward, robust solution for reaching elevated work areas. Manufactured from lightweight yet strong aluminum alloy, it leans safely against walls and structures with its slip-resistant rubber feet. Ideal for guttering, window cleaning, and exterior painting on standard residential properties.</p>",
        "features": "Lightweight aluminum construction\nSlip-resistant rubber feet and top hooks\nDeep-grooved anti-slip rungs\nFixed single-section design for simplicity and reliability\nMounting hooks for wall or roof edge use\nMaximum load: 120 kg\nAvailable in 4m, 5m, 6m lengths"
    },
    {
        "name": "Aluminium Extension Ladder with Stabilizer Bar 5",
        "desc": "<p>Our <strong>Extension Ladder with Stabilizer Bar</strong> adds a wide V-shaped standoff bar to keep the ladder safely away from the wall and provide exceptional lateral stability. The stabilizer prevents the ladder from slipping sideways on smooth wall surfaces and gives working access to gutters, roofline, and fascia boards without obstruction.</p>",
        "features": "V-shaped stabilizer bar for lateral stability and wall standoff\nAdjustable stabilizer fits various ladder widths\nHeavy-duty aluminum ladder with anti-slip rungs\nRubber-tipped stabilizer ends protect wall surfaces\nExtends safely to 7 meters\nMaximum load: 150 kg\nFolds flat for transport"
    },
    {
        "name": "Professional Roof Access Aluminium Extension Ladder 6",
        "desc": "<p>Specifically engineered for safe roof access, the <strong>Roof Access Extension Ladder</strong> features roof hooks at the top section that anchor securely over a roof ridge for hands-free stability. The extra-long overlapping sections provide maximum height adjustment flexibility, while the heavy-duty rungs support continuous professional use by roofing contractors and maintenance crews.</p>",
        "features": "Roof ridge hooks for secure hands-free anchorage\nTwo-section overlap design for height flexibility\nHeavy-duty extruded aluminum construction\nAnti-slip serrated rungs with comfort grip\nAdjustable rubber feet for uneven ground\nMaximum load: 150 kg\nComplies with BS EN131 roofing standards"
    },
    {
        "name": "Telescopic Ladder with Self-Locking System 7",
        "desc": "<p>The <strong>Self-Locking Telescopic Ladder</strong> incorporates a patented dual-action safety lock on each rung that requires deliberate two-handed operation to collapse, making accidental retraction virtually impossible during use. Each section locks positively with an audible click, and the ergonomic pull cord allows smooth one-handed extension.</p>",
        "features": "Patented dual-action safety lock on each rung\nDeliberate two-handed collapse mechanism for safety\nAudible click confirms positive rung lock engagement\nErgonomic pull cord for smooth one-handed extension\nCompact collapsed length: 92cm\nMaximum extension: 6.2 meters\nMaximum load: 150 kg"
    },
    {
        "name": "Slim-Profile Aluminium Telescopic Ladder 8",
        "desc": "<p>The <strong>Slim-Profile Telescopic Ladder</strong> is designed for space-constrained storage in vans, workshops, and apartments. With a collapsed width of just 37cm and a featherlight weight of only 7.5 kg, it travels with you effortlessly. Despite its slim dimensions, it provides full-rated load capacity and the same safety certifications as our standard professional range.</p>",
        "features": "Ultra-slim collapsed profile: 37cm width\nFeatherlight at just 7.5 kg\nFull EN131 rated load capacity\nAnti-slip rungs with slip-resistant rubber feet\nIdeal for vans, apartments, and tight storage spaces\nExtends to 5 meters\nMaximum load: 150 kg"
    },
    {
        "name": "Wide-Step Aluminium Extension Ladder 9",
        "desc": "<p>The <strong>Wide-Step Extension Ladder</strong> features extra-deep, 30mm wider-than-standard rungs that significantly reduce foot fatigue during long working sessions at height. The widened rungs also improve safety by making it harder to miss a step when descending. Ideal for painters, plasterers, and anyone who spends extended periods working from a ladder.</p>",
        "features": "Extra-wide 30mm deeper rungs reduce foot fatigue\nImproved safety on descent with wider step profile\nHeavy-duty aluminum extrusion frame\nTwo-section design with positive-click rungs\nAnti-slip rubber feet with ground spike option\nMaximum load: 150 kg\nExtends to 6 meters"
    },
    {
        "name": "Folding Aluminium Extension Ladder 10",
        "desc": "<p>The <strong>Folding Aluminium Extension Ladder</strong> combines the convenience of a fold-flat design with the reach of a full extension ladder. The articulated hinge points allow the ladder to fold completely flat for vehicle transport or slim upright storage, then deploy quickly to a rigid extension configuration. Perfect for trade professionals who need maximum versatility from a single piece of access equipment.</p>",
        "features": "Fold-flat hinge design for vehicle transport and slim storage\nDeploys quickly from folded to extension configuration\nArticulated hinge with positive-lock mechanism\nAnti-slip rungs and rubber feet\nFolds to 95cm x 37cm x 8cm\nMaximum load: 150 kg\nExtends to 6.5 meters"
    },
    # ─── MULTI-PURPOSE / COMBINATION LADDERS (11–22) ──────────
    {
        "name": "Multi-Function 4-Section Folding Aluminium Ladder 11",
        "desc": "<p>The <strong>Multi-Function 4-Section Combination Ladder</strong> is the ultimate 4-in-1 versatile ladder engineered for professional and home use. Its patented hinge-joint technology allows it to transform into a step ladder, extension ladder, staircase ladder, or scaffold base in seconds. Constructed from heavy-duty extruded aluminum, each section features deeply grooved rungs for superior grip.</p>",
        "features": "4-in-1: Step / Extension / Staircase / Scaffold base\nHeavy-duty extruded aluminum, anodized finish\nPatented multi-pivot hinge joints with spring-loaded locks\nExtra-wide anti-slip rungs with textured surface\nMaximum load capacity: 150 kg\nFolds flat for easy storage\nComplies with EN131"
    },
    {
        "name": "Multi-Function Combination Ladder with Work Platform 12",
        "desc": "<p>Our <strong>Combination Ladder with Work Platform</strong> upgrades the classic multi-function design with a wide, non-slip work platform at the top apex. The platform provides a safe, flat standing surface during overhead tasks, eliminating the discomfort of standing on a single rung. The integrated hand rail gives additional security for high-reach work.</p>",
        "features": "Wide non-slip top work platform at apex\nIntegrated handrail for high-reach security\n4-in-1 convertible configuration system\nDeep-grooved aluminum rungs throughout\nWide-stance feet with rubber end caps\nMaximum load: 150 kg\nEN131 certified"
    },
    {
        "name": "Heavy-Duty 5-Section Aluminium Combination Ladder 13",
        "desc": "<p>The <strong>5-Section Combination Ladder</strong> extends our multi-function range to provide even greater reach in extension ladder mode — up to 8 meters — while still folding down to a compact and manageable carry size. Five individually adjustable sections offer unmatched flexibility for construction sites, high-ceiling maintenance, and professional building services.</p>",
        "features": "5 individually adjustable sections for 8m reach\nCompact folded size despite extended reach\nHeavy-duty hinge joints rated for continuous professional use\nAnti-slip serrated rungs throughout\nMaximum load: 150 kg\nBuilt-in carry handle\nEN131 and AS/NZS 1892 certified"
    },
    {
        "name": "Aluminium Scaffold Tower Combination Ladder 14",
        "desc": "<p>The <strong>Scaffold Tower Combination Ladder</strong> includes a detachable scaffold plank accessory that transforms the ladder base into a stable working platform at mid-height. The plank bridges across the open legs of the A-frame configuration, providing a wide, flat surface for painting, plastering, and inspection tasks up to 1.5 meters working height.</p>",
        "features": "Includes detachable wide scaffold plank accessory\nTransforms to stable working platform at 1.5m\nA-frame configuration with locking spreader bar\nHeavy-duty aluminum construction\nPlatform-rated load: 100 kg\nLadder load: 150 kg\nEasy assembly without tools"
    },
    {
        "name": "Articulating Multi-Position Access Ladder 15",
        "desc": "<p>The <strong>Articulating Multi-Position Access Ladder</strong> provides unmatched flexibility with four independently adjustable sections and multiple locking hinge joints. It can be configured as a standard A-frame, a straight extension, an angled staircase ladder, or a 90-degree wall brace — adapting instantly to complex access challenges on construction sites and complex architectural environments.</p>",
        "features": "Four independently adjustable sections\nMultiple hinge joints at independent positions\nStaircase mode for safe use on stairs\n90-degree wall brace configuration\nHeavy-duty anodized aluminum\nMaximum load: 150 kg\nAll positions EN131 certified"
    },
    {
        "name": "Compact Folding Multipurpose Ladder 16",
        "desc": "<p>The <strong>Compact Folding Multipurpose Ladder</strong> is the ideal tool for domestic and light trade use where storage space is at a premium. Folding to just 95cm in any configuration, it fits easily in a car boot, under stairs, or in a hallway cupboard. Despite its compact size, it provides full-rated load capacity and all four working configurations.</p>",
        "features": "Folds to just 95cm in any configuration\nFits in a standard car boot or under stairs\nAll four working configurations available\nFull-rated 150 kg load capacity\nLightweight at just 9 kg\nAnti-slip rungs and rubber feet\nIdeal for domestic and light trade use"
    },
    {
        "name": "Professional Grade Aluminium Combination Ladder 17",
        "desc": "<p>The <strong>Professional Grade Combination Ladder</strong> is built to withstand the rigors of continuous daily use on commercial construction sites. The frame extrusions are 20% thicker than standard consumer models, the hinge joints are machined to tighter tolerances, and all hardware is zinc-plated for corrosion resistance. Designed to perform flawlessly for 10+ years of hard professional use.</p>",
        "features": "20% thicker frame extrusions than consumer models\nTighter-tolerance machined hinge joints\nZinc-plated hardware for corrosion resistance\nDesigned for 10+ years of daily professional use\nMaximum load: 150 kg\nAll configurations EN131 certified\nFull manufacturer's warranty"
    },
    {
        "name": "Lightweight DIY Combination Ladder 18",
        "desc": "<p>The <strong>Lightweight DIY Combination Ladder</strong> brings the power of a professional multi-function ladder to the home user at an approachable weight of just 8.5 kg. Perfect for changing light fittings, painting rooms, accessing loft hatches, and cleaning high windows. The intuitive hinge system reconfigures in under 30 seconds without tools.</p>",
        "features": "Featherlight at just 8.5 kg\nReconfigures in under 30 seconds without tools\nIntuitive color-coded hinge locking system\nAnti-slip rungs and non-marking rubber feet\nIdeal for domestic DIY applications\nMaximum load: 120 kg\nCompact storage footprint"
    },
    {
        "name": "Double-Sided Step & Extension Combination Ladder 19",
        "desc": "<p>The <strong>Double-Sided Step & Extension Combination Ladder</strong> features full-length rungs accessible from both sides of the A-frame, allowing two people to use the ladder simultaneously from opposite sides. This unique design doubles productivity on wide-area tasks like tree pruning, mural painting, and large-scale ceiling work.</p>",
        "features": "Full-length rungs accessible from both A-frame sides\nAllows simultaneous use by two people\nHeavy-duty aluminum frame with reinforced rungs\nRated for two-person load (combined 160 kg)\nLocking spreader bar with positive-click mechanism\nMaximum single-user load: 150 kg\nEN131 certified"
    },
    {
        "name": "Telescoping Multi-Position Platform Ladder 20",
        "desc": "<p>The <strong>Telescoping Multi-Position Platform Ladder</strong> combines the reach of a telescopic ladder with the stability of a wide top platform. Four adjustable leg positions allow each leg to be independently set on staircase steps, uneven terrain, or sloping surfaces, ensuring a perfectly level working platform regardless of ground conditions.</p>",
        "features": "Four independently adjustable leg positions\nPerfectly level platform on stairs and slopes\nWide top platform with non-slip surface\nTelescopic legs for height fine-tuning\nSpirit level built into platform\nMaximum load: 150 kg\nEN131 and BS 8620 certified"
    },
    {
        "name": "Aluminium A-Frame Household Step Ladder 21",
        "desc": "<p>Our <strong>Aluminium A-Frame Household Step Ladder</strong> is a timeless, reliable design optimized for everyday home tasks. With its clean, simple A-frame construction, automatic spreader lock, and lightweight aluminum build, it is the go-to ladder for kitchen tasks, changing bulbs, accessing high shelves, and basic DIY work.</p>",
        "features": "Classic A-frame design with automatic spreader lock\nLightweight aluminum construction\nFlat, non-slip step rungs\nRubber feet prevent floor marking and sliding\nAvailable in 3, 4, 5, and 6-step heights\nMaximum load: 120 kg\nFolds thin for cupboard storage"
    },
    {
        "name": "Aluminium Folding Step & Work Platform Ladder 22",
        "desc": "<p>The <strong>Folding Step & Work Platform Ladder</strong> is a professional-grade, all-in-one step ladder and work platform. Designed for plastering, tiling, electrical installation, and general maintenance, the wide ribbed-aluminum platform provides ample standing room for extended work sessions. Heavy-duty locking hinges and a low-centre-of-gravity design provide exceptional stability.</p>",
        "features": "Wide ribbed aluminum work platform for extended sessions\nHeavy-duty locking hinges throughout\nLow-centre-of-gravity design for superior stability\nDeep non-slip step rungs\nFolds flat to 18cm depth for storage\nMaximum load: 150 kg\nEN131 and OSHA compliant"
    },
    # ─── STEP LADDERS (23–32) ─────────────────────────────────
    {
        "name": "Professional Platform Step Ladder with Tool Tray 23",
        "desc": "<p>Our <strong>Professional Platform Step Ladder</strong> features a wide, non-slip standing platform at the top for maximum comfort and safety during extended overhead work. The integrated heavy-gauge tool tray keeps tools, paint tins, and materials within arm's reach, eliminating dangerous trips up and down. The A-frame design with locking spreader bar ensures rock-solid stability.</p>",
        "features": "Wide non-slip top platform for safe standing and kneeling\nIntegrated heavy-gauge tool tray at the top\nA-frame design with automatic spreader bar lock\nDeep-grooved anti-skid aluminum steps\nHeavy-duty riveted frame construction\nMaximum load: 120 kg\nFolds flat for compact storage"
    },
    {
        "name": "Fibreglass Step Ladder – Electrician Safe 24",
        "desc": "<p>The <strong>Fibreglass Step Ladder</strong> is the essential safety tool for electricians, linemen, and anyone working near live electrical equipment. The non-conductive fibreglass side rails and rungs provide full electrical insulation, protecting the user from accidental contact with live conductors. Rated to 1000V AC for complete peace of mind during electrical work.</p>",
        "features": "Non-conductive fibreglass side rails and rungs\nRated to 1000V AC for electrical safety\nHeavy-duty aluminum reinforcement channels\nDeep anti-slip step rungs\nRubber feet prevent slipping on all surfaces\nMaximum load: 150 kg\nEN131 electrician grade certified"
    },
    {
        "name": "Wide-Base Safety Step Ladder 25",
        "desc": "<p>The <strong>Wide-Base Safety Step Ladder</strong> features a significantly wider-than-standard leg base for dramatically improved stability on all surfaces. The wide stance reduces the risk of the ladder tipping sideways under an off-center load, making it ideal for heavier trades workers and for use on polished or slippery floor surfaces such as in commercial kitchens, hospitals, and retail spaces.</p>",
        "features": "Extra-wide leg base for dramatically improved stability\nReduces side-tipping risk under off-center loads\nIdeal for polished/slippery commercial floor surfaces\nDeep anti-slip aluminum step rungs\nAutomatic spreader bar lock\nMaximum load: 130 kg\nEN131 certified"
    },
    {
        "name": "Lightweight Aluminium 3-Step Kick Stool Ladder 26",
        "desc": "<p>The <strong>3-Step Kick Stool Ladder</strong> is the perfect compact access solution for retail environments, libraries, and domestic kitchens. Its small footprint and zero-assembly operation make it instantly ready when you need to reach that high shelf. The non-marking rubber feet and all-aluminum construction make it equally at home in premium commercial settings and modern kitchens.</p>",
        "features": "Zero-assembly, instant-use design\nSmall footprint for retail and domestic spaces\nNon-marking rubber feet protect all floor types\nLightweight at just 3.5 kg\nAutomatic locking A-frame for stability\nMaximum load: 100 kg\nAvailable in silver and black finishes"
    },
    {
        "name": "Heavy-Duty Industrial Step Ladder 27",
        "desc": "<p>The <strong>Heavy-Duty Industrial Step Ladder</strong> is built to ANSI Type 1AA standards for the most demanding industrial environments. The extra-thick aluminum extrusions, all-riveted construction, and industrial-grade rubber feet deliver unwavering performance in warehouses, factories, and heavy construction. Supports up to 170 kg for use by heavier workers in full PPE.</p>",
        "features": "ANSI Type 1AA industrial grade construction\nExtra-thick aluminum extrusions throughout\nAll-riveted frame for maximum structural integrity\nIndustrial-grade non-slip rubber feet\nMaximum load: 170 kg (extra-heavy duty rated)\nReinforced spreader bar and locking mechanism\nFull OSHA compliance"
    },
    {
        "name": "Folding Step Stool – Slim Design 28",
        "desc": "<p>The <strong>Folding Step Stool Slim Design</strong> brings clever engineering to a simple everyday need. At just 4cm folded thickness, it slides between appliances, behind doors, and under beds for truly out-of-sight storage. The lightweight aluminum frame and anti-slip rubber feet provide safe and stable assistance for reaching high cupboards, shelves, and overhead storage.</p>",
        "features": "Ultra-slim: folds to just 4cm thickness\nSlides between appliances and behind doors\nLightweight aluminum frame — just 2.8 kg\nAnti-slip rubber feet prevent sliding\nNon-slip top step surface\nMaximum load: 100 kg\nIdeal for kitchens, bathrooms, and offices"
    },
    {
        "name": "Adjustable-Height Step Platform Ladder 29",
        "desc": "<p>The <strong>Adjustable-Height Step Platform Ladder</strong> allows the platform height to be independently adjusted on each side, making it perfectly level on staircases and sloped surfaces. The wide aluminum work platform provides a stable base for painting, wallpapering, and tiling on stairs and split-level areas where conventional step ladders cannot be safely used.</p>",
        "features": "Independent height adjustment on each side leg\nLevel working platform on stairs and slopes\nWide ribbed aluminum work platform\nHeavy-duty locking adjustment mechanism\nNon-slip rubber feet throughout\nMaximum load: 130 kg\nIdeal for staircase painting and papering"
    },
    {
        "name": "Compact Folding 2-Step Aluminium Stool 30",
        "desc": "<p>The <strong>Compact Folding 2-Step Aluminium Stool</strong> is the ultimate minimalist step stool for domestic use. Opening and closing in one single motion, it provides a stable two-rung boost for kitchen, bathroom, and bedroom access needs. The all-aluminum construction will never rust or rot, making it the last step stool you will ever need to buy.</p>",
        "features": "One-motion open and close mechanism\nUltra-compact folded footprint\nAll-aluminum construction — rust and rot free\nAnti-slip rubber feet and top surface\nMaximum load: 100 kg\nAvailable in 2 and 3-step heights\nLifetime structural warranty"
    },
    {
        "name": "Multi-Step Platform Ladder with Guardrail 31",
        "desc": "<p>The <strong>Multi-Step Platform Ladder with Guardrail</strong> provides the additional security of a handrail surround on the work platform, suitable for the elderly, less able users, and any professional requiring three points of contact at height. The wrap-around guardrail prevents accidental falls from the platform and gives confidence when leaning out to reach during ceiling and high-wall tasks.</p>",
        "features": "Full wrap-around platform guardrail for fall prevention\nSuitable for elderly and less able users\nThree-point contact at height\nWide non-slip aluminum work platform\nHeavy-duty A-frame construction\nMaximum load: 130 kg\nEN131 and BS 2037 compliant"
    },
    {
        "name": "Professional Double-Sided Step Ladder 32",
        "desc": "<p>The <strong>Professional Double-Sided Step Ladder</strong> provides fully accessible steps on both sides of the A-frame, allowing two users to work simultaneously from either face. Ideal for hanging large artwork, installing suspended ceilings, and setting up event staging where two workers need access to the same elevated area simultaneously.</p>",
        "features": "Fully accessible rungs on both sides of A-frame\nAllows simultaneous two-person use\nHeavy-duty aluminum frame and rungs\nLocking spreader bar for absolute stability\nMaximum combined load: 180 kg\nMaximum single-user load: 150 kg\nEN131 certified two-person use"
    },
    # ─── LADDER HARDWARE COMPONENTS (33–42) ───────────────────
    {
        "name": "Aluminium Ladder Hinge Joint Connector Set 33",
        "desc": "<p>The <strong>Aluminium Ladder Hinge Joint Connector Set</strong> is a premium hardware replacement and upgrade kit for multi-function combination ladders. Each hinge joint is precision-forged from high-tensile aluminum alloy with a durable powder-coat finish for maximum corrosion resistance. The multi-position locking mechanism engages at multiple angles.</p>",
        "features": "Precision-forged high-tensile aluminum alloy\nMulti-position locking at 90°, 135°, and 180°\nHardened steel pivot pin with anti-corrosion treatment\nFits standard 30mm and 35mm side rails\nIncludes mounting hardware and guide\nCompatible with most aluminum combination ladders\nDurable powder-coat finish"
    },
    {
        "name": "Heavy-Duty Ladder Hinge Pivot Joint 34",
        "desc": "<p>The <strong>Heavy-Duty Ladder Hinge Pivot Joint</strong> is the industrial-grade version of our standard hinge connector, featuring thicker aluminum casting and a larger-diameter hardened steel pivot pin rated for 200 kg continuous load. Designed as a direct replacement for worn hinge joints in heavy-duty commercial ladders and as an OEM component for ladder manufacturers.</p>",
        "features": "Industrial-grade thicker aluminum casting\nLarger-diameter hardened steel pivot pin\nRated for 200 kg continuous load\nPositive multi-angle locking mechanism\nDirect OEM replacement for commercial ladders\nAnti-corrosion phosphate and powder-coat finish\nIncludes all mounting hardware"
    },
    {
        "name": "Aluminium Ladder Step Rung Replacement Set 35",
        "desc": "<p>Our <strong>Aluminium Ladder Step Rung Replacement Set</strong> contains everything needed to replace worn, damaged, or bent rungs on aluminium ladders of all types. Each rung is precision-extruded from 6061-T6 aluminum with deep anti-slip serrations machined into the top surface. Available in multiple widths and depths to match all common ladder profiles.</p>",
        "features": "Precision-extruded 6061-T6 aluminum\nDeep anti-slip serrations machined into top surface\nMultiple widths and depths for all ladder profiles\nIncludes replacement rivets and installation tool\nRestores ladder to full rated load capacity\nAnodized finish matches standard ladder aesthetics\nFits most aluminum A-frame and extension ladders"
    },
    {
        "name": "Heavy-Duty Ladder Spreader Bar & Corner Bracket Kit 36",
        "desc": "<p>Our <strong>Spreader Bar & Corner Bracket Kit</strong> provides the critical structural support for safe A-frame step ladder use. The powder-coated red steel spreader bar limits outward splay, while the precision-engineered corner brackets reinforce the frame at its most stress-intensive points. Each bracket features multiple bolt holes for a rock-solid, adjustable fit.</p>",
        "features": "High-grade steel spreader bar with red powder coating\nPrevents dangerous outward splay of ladder legs\nCorner brackets reinforce high-stress frame joints\nMultiple bolt holes for universal fit\nCompatible with most A-frame step ladders\nAll mounting hardware included\nRated for load capacities up to 150 kg"
    },
    {
        "name": "Aluminium Ladder Side Rail Profile – Square Section 37",
        "desc": "<p>The <strong>Aluminium Ladder Side Rail Profile – Square Section</strong> is the structural backbone of heavy-duty aluminium ladders. Precision-extruded from 6061-T6 alloy with a square tubular cross-section for maximum torsional rigidity, it is available in standard and custom dimensions for ladder manufacturers, professional repair workshops, and prototype fabricators.</p>",
        "features": "6061-T6 aluminum alloy square tubular extrusion\nMaximum torsional rigidity for ladder side rails\nPrecision anodized surface finish\nStandard cross-section: 35mm x 35mm x 2.5mm wall\nAvailable in lengths from 1m to 6m\nUsed in manufacturing and repairing professional ladders\nCustom dimensions available on request"
    },
    {
        "name": "Aluminium Ladder Side Rail Profile – Rectangular Section 38",
        "desc": "<p>The <strong>Rectangular Section Side Rail Profile</strong> offers superior bending resistance in the vertical loading plane for ladder side rails. The asymmetric rectangular cross-section concentrates material where it provides the most structural benefit under typical ladder loads, delivering a higher safety factor for the same weight compared to square sections.</p>",
        "features": "6061-T6 aluminum alloy rectangular extrusion\nSuperior bending resistance in vertical loading plane\nAsymmetric cross-section for optimum weight efficiency\nStandard size: 30mm x 50mm x 2mm wall\nPrecision anodized finish\nAvailable in 1m to 6m standard lengths\nCustom dimensions available"
    },
    {
        "name": "Anti-Slip Rubber Ladder Feet Set – Standard Size 39",
        "desc": "<p>Our <strong>Anti-Slip Rubber Ladder Feet Set</strong> is the essential safety upgrade for any aluminium ladder. Moulded from premium natural rubber with a deep tread pattern, these feet dramatically increase friction on all surfaces including smooth tiles, polished concrete, and outdoor ground. The precision-fit design ensures a snug, non-twisting fit on standard aluminium side rail ends.</p>",
        "features": "Premium natural rubber with deep anti-slip tread\nDramatically increases grip on smooth and wet surfaces\nPrecision-fit for standard aluminum side rails\nTop rail caps included to protect walls\nResistant to oil, grease, and chemicals\nEasy tool-free snap-on installation\nSet of 4 feet caps + 2 top rail caps"
    },
    {
        "name": "Extra-Large Heavy-Duty Rubber Ladder Feet Set 40",
        "desc": "<p>The <strong>Extra-Large Heavy-Duty Rubber Ladder Feet Set</strong> provides even greater ground contact area for maximum friction on slippery surfaces. The enlarged footprint is particularly effective on loose gravel, wet grass, smooth tiles, and polished stone — surfaces where standard ladder feet may be inadequate. Includes a ground spike insert for use on soft outdoor ground.</p>",
        "features": "Extra-large footprint for maximum surface contact\nHigh-friction compound for slippery surfaces\nOptional ground spike insert for soft outdoor use\nFits standard and oversized aluminum side rails\nHeavy-duty construction for industrial use\nEasy tool-free installation\nSet of 4 oversized feet"
    },
    {
        "name": "Ladder Wall Protection Bumpers – Rubber 41",
        "desc": "<p>The <strong>Ladder Wall Protection Bumpers</strong> are soft rubber caps designed to protect walls, window frames, and rendered surfaces from damage caused by the top of an aluminium ladder leaning against them. The large contact area spreads the ladder's load across a wider surface and the soft rubber compound eliminates scratching, gouging, and paint damage.</p>",
        "features": "Soft rubber protects walls from scratching and gouging\nLarge contact area spreads load for no surface damage\nFits standard aluminum side rail top ends\nNon-marking compound for all wall types\nIncludes secure fitting strap\nPair of 2 bumpers included\nIdeal for use on plastered and painted walls"
    },
    {
        "name": "Heavy-Duty Ladder Locking Hinge Assembly 42",
        "desc": "<p>The <strong>Heavy-Duty Ladder Locking Hinge Assembly</strong> is a complete, ready-to-install hinge unit including all bolts, washers, locking pins, and a new pivot axle for the full rehabilitation of a worn or damaged multi-function ladder hinge point. Manufactured to OEM specifications for direct compatibility with the most common aluminium combination ladder brands.</p>",
        "features": "Complete rehabilitation kit for worn ladder hinges\nAll bolts, washers, locking pins, and pivot axle included\nManufactured to OEM specifications\nCompatible with most combination ladder brands\nHardened steel pivot with anti-corrosion coating\nPrecision-machined aluminum hinge body\nFull installation instructions included"
    },
    # ─── CARGO STRAPS / LASHING BELTS (43–50) ────────────────
    {
        "name": "Heavy-Duty Lashing Strap with Cam Buckle 25mm 43",
        "desc": "<p>Our <strong>25mm Cam Buckle Lashing Strap</strong> is the ideal size for securing motorcycles, lightweight machinery, and furniture on trailers and moving trucks. The narrow 25mm strap threads easily through tight anchor points, and the ergonomic zinc-alloy cam buckle provides smooth, one-handed tensioning. Includes two soft loops to protect delicate painted surfaces from strap abrasion.</p>",
        "features": "High-tenacity polyester webbing, 25mm width\nZinc-alloy cam buckle for one-handed tightening\nSafe working load: 150 kg; Break strength: 450 kg\nIncludes 2 soft loops to protect painted surfaces\nUV and moisture resistant construction\nAvailable in blue, orange, green, and red\nComplies with EN12195-2"
    },
    {
        "name": "Heavy-Duty Lashing Strap with Cam Buckle 38mm 44",
        "desc": "<p>Our <strong>38mm Cam Buckle Lashing Strap</strong> is the most popular all-around cargo securing strap for trade professionals. Precision-stitched high-tenacity polyester webbing delivers consistent 800 kg tensile strength, while the robust zinc-alloy cam buckle provides secure, one-motion locking. Resists UV, moisture, and most chemicals in all-weather outdoor use.</p>",
        "features": "High-tenacity polyester webbing, 38mm width\nZinc-alloy cam buckle, one-motion locking\nTensile strength: 800 kg; SWL: 250 kg\nUV, moisture, and chemical resistant\nAvailable in orange, blue, green, black, yellow\nComplies with EN12195-2\nPrecision stitching throughout"
    },
    {
        "name": "Heavy-Duty Ratchet Tie-Down Strap 50mm 45",
        "desc": "<p>The <strong>50mm Ratchet Tie-Down Strap</strong> provides the highest level of cargo securing tension available in a manual strap. The ratchet mechanism multiplies your applied force to achieve tensions impossible with cam buckle straps, making it the definitive choice for securing large machinery, vehicles, boats, and shipping containers. Complies with EN12195-2 Grade 2 lashing standard.</p>",
        "features": "High-tenacity polyester webbing, 50mm width\nHeavy-duty ratchet mechanism for maximum tension\nSafe working load: 2500 kg; Break strength: 5000 kg\nDouble J-hook fittings for positive anchorage\nUV, chemical, and moisture resistant\nComplies with EN12195-2 Grade 2\nAvailable in standard and long-reach lengths"
    },
    {
        "name": "Polyester Cargo Strap with E-Track Fitting 46",
        "desc": "<p>The <strong>Cargo Strap with E-Track Fitting</strong> is purpose-designed for vehicles fitted with E-track logistic rail systems. The precision-engineered E-track end fitting clicks securely into any E-track or A-track rail, eliminating the need for separate anchor points. Ideal for logistics operators, removals companies, and cargo van conversions.</p>",
        "features": "E-track/A-track end fitting for logistic rail systems\nHigh-tenacity polyester webbing, 50mm width\nCam buckle or ratchet version available\nClicks securely into any standard E-track rail\nSWL: 500 kg; Break strength: 1500 kg\nUV and moisture resistant\nIdeal for cargo van conversions and logistics"
    },
    {
        "name": "Heavy-Duty Multi-Loop Tie-Down Set 47",
        "desc": "<p>The <strong>Multi-Loop Tie-Down Set</strong> includes four 38mm ratchet straps with a mix of J-hook and flat hook end fittings for maximum versatility. Pre-sorted into a robust woven carry bag, this set is the complete cargo security solution for tradespeople, farmers, and transport operators who need reliable load securing for every job.</p>",
        "features": "Set of 4 x 38mm ratchet tie-down straps\nMix of J-hook and flat hook end fittings\nHigh-tenacity polyester webbing throughout\nSWL per strap: 500 kg\nRobust woven carry bag included\nUV, moisture, and chemical resistant\nComplies with EN12195-2"
    },
    {
        "name": "Polyester Flat Woven Lashing Webbing Roll 48",
        "desc": "<p>Our <strong>Polyester Flat Woven Lashing Webbing Roll</strong> is sold by the metre for fabricating custom tie-down assemblies, slings, and cargo securing equipment. Woven from high-tenacity polyester yarns to a consistent 50mm width and 2mm thickness, it maintains its rated tensile strength across the full roll with no join points or weak spots.</p>",
        "features": "High-tenacity polyester, 50mm width, 2mm thickness\nNo joins — full length consistent strength\nBreak strength: 2500 kg per 50mm width\nUV, moisture, and abrasion resistant\nIdeal for custom tie-down and sling fabrication\nSold per metre or in 100m rolls\nAvailable in multiple colors"
    },
    {
        "name": "Bungee Cord Cargo Net – Heavy Duty 49",
        "desc": "<p>Our <strong>Bungee Cord Cargo Net</strong> provides flexible, stretch-fit cargo retention for motorcycles, bicycles, lightweight luggage, and small items on open trailers and pickup beds. The heavy-duty bungee cords and stainless steel hooks stretch to accommodate irregularly shaped loads while maintaining consistent tension throughout the journey.</p>",
        "features": "Heavy-duty bungee cord construction with elastic stretch\nStainless steel hook clips at all corners\nStretches to accommodate irregular load shapes\nMaintains consistent tension throughout journey\nIdeal for motorcycles, bicycles, and small cargo\nWeather resistant and UV stabilized\nMultiple size options available"
    },
    {
        "name": "Adjustable Cargo Bar for Vans & Trucks 50",
        "desc": "<p>The <strong>Adjustable Cargo Bar</strong> provides a simple, tool-free solution for dividing van and truck cargo areas into separate zones, preventing load shift during transit. The spring-loaded telescopic bar adjusts to fit all standard commercial vehicle widths and applies firm lateral pressure against the vehicle sides. Rubber-tipped ends protect vehicle walls from damage.</p>",
        "features": "Spring-loaded telescopic design for tool-free adjustment\nFits all standard commercial vehicle widths\nFirm lateral pressure prevents load shift\nRubber-tipped ends protect vehicle walls\nHeavy-duty steel with anti-corrosion coating\nRated lateral force: 200 kg\nInstalls in seconds without tools"
    },
    # ─── ROPES (51–57) ────────────────────────────────────────
    {
        "name": "High-Strength Braided Nylon Safety Rope 10mm 51",
        "desc": "<p>Our <strong>10mm Braided Nylon Safety Rope</strong> is manufactured from virgin high-tenacity nylon yarns using a tight 16-strand braiding process that maximises tensile strength and minimises stretch. Designed for construction safety lines, load hoisting, marine mooring, and demanding outdoor recreation. UV stabilizers ensure long-term color and strength retention.</p>",
        "features": "Virgin high-tenacity nylon, 16-strand braid\nDiameter: 10mm; Break strength: ~1200 kg\nExcellent elasticity for shock load absorption\nUV-stabilized for long-term outdoor use\nSmooth braid for easy passage through pulleys\nResistant to abrasion, rot, and marine chemicals\nAvailable in 10m, 20m, 30m, 50m lengths"
    },
    {
        "name": "Heavy-Duty Twisted Polyester Anchor Rope 12mm 52",
        "desc": "<p>The <strong>12mm Twisted Polyester Anchor Rope</strong> combines high tensile strength with very low stretch — a critical requirement for anchor lines, mooring, rigging, and load control applications where dimensional stability under load is essential. Unlike nylon, polyester retains its full strength when wet and in extended submersion.</p>",
        "features": "3-strand twisted polyester construction, 12mm diameter\nVery low stretch for precise load control\nRetains full strength when wet and submerged\nHigh UV and abrasion resistance\nBreak strength: ~1500 kg\nSmooth surface for pulley and winch use\nAvailable in various colors and lengths"
    },
    {
        "name": "Reflective Braided Polyester Safety Line 8mm 53",
        "desc": "<p>The <strong>8mm Reflective Braided Polyester Safety Line</strong> incorporates highly visible reflective tracer threads woven into the outer braid, creating brilliant illumination when caught by torchlight or vehicle headlights. An essential safety item for evening and nighttime camping, hiking, and marine operations where rope visibility is a critical safety factor.</p>",
        "features": "Highly reflective tracer threads in outer braid\nBrilliant illumination in low light conditions\n8mm diameter polyester construction\nHigh UV and weather resistance\nBreak strength: ~800 kg\nIdeal for camping, hiking, and marine use\nAvailable in fluorescent color options"
    },
    {
        "name": "High-Tenacity Polypropylene Multi-Purpose Rope 6mm 54",
        "desc": "<p>Our <strong>6mm Polypropylene Multi-Purpose Rope</strong> is the lightweight, economical general-purpose rope for everyday bundling, tying, and securing tasks. It floats on water, is resistant to most common acids and alkalis, and its bright colors ensure high visibility in any setting. Available in bulk rolls for trade buyers and shorter lengths for retail.</p>",
        "features": "Floats on water — ideal for marine and poolside use\nBright colors for high visibility\nResistant to most acids, alkalis, and chemicals\n6mm diameter; break strength: ~350 kg\nLightweight and easy to handle and store\nAvailable in bulk rolls or cut lengths\nIdeal for bundling, tying, and general securing"
    },
    {
        "name": "Double-Braided Polyester Halyard Rope 10mm 55",
        "desc": "<p>The <strong>Double-Braided Polyester Halyard Rope</strong> uses a high-strength polyester core inside a protective polyester outer braid. This construction delivers superior strength, very low elongation, and excellent resistance to the cyclic loading of sailing halyards and flag poles. The smooth outer braid runs easily through blocks, clutches, and cleats without snagging.</p>",
        "features": "Double-braid construction: polyester core + polyester cover\nVery low elongation for precise sail control\nSmooth outer braid for easy block and cleat operation\nExcellent cyclic load fatigue resistance\nBreak strength: ~1200 kg\nUV and saltwater resistant\nAvailable in multiple colors and lengths"
    },
    {
        "name": "Industrial Shock Absorbing Bungee Rope 10mm 56",
        "desc": "<p>Our <strong>Industrial Shock Absorbing Bungee Rope</strong> combines an ultra-high-elongation latex rubber core with a protective braided polyester sleeve. It absorbs sudden shock loads that would damage rigid ropes, making it ideal for load lashing on vehicles, elastic mooring systems, and safety backup lines in industrial lifting applications.</p>",
        "features": "Ultra-high-elongation latex rubber core\nProtective braided polyester outer sleeve\nExcellent shock load absorption\n10mm diameter; maximum elongation: 100%\nResistant to UV, ozone, and weather\nIdeal for vehicle lashing and elastic mooring\nAvailable in standard and custom lengths"
    },
    {
        "name": "Colorful Braided Nylon Decoration & Craft Rope 5mm 57",
        "desc": "<p>Our <strong>5mm Braided Nylon Decoration & Craft Rope</strong> is available in a wide range of vibrant colors for macramé, craft projects, home decor, pet accessories, and novelty applications. The smooth, tightly braided construction holds knots securely, takes dye evenly, and resists fraying at cut ends. Sold in convenient cut lengths or bulk rolls.</p>",
        "features": "Available in 20+ vibrant colors\nSmooth tight braid for crafts and macramé\nHolds knots securely and resists fraying\nTakes dye evenly for custom color projects\n5mm diameter; break strength: ~200 kg\nIdeal for macramé, pet toys, and home decor\nSold in cut lengths or bulk rolls"
    },
    # ─── CARGO NETS & ACCESSORIES (58–63) ────────────────────
    {
        "name": "Heavy-Duty Cargo Net with Carabiner Hooks 58",
        "desc": "<p>Our <strong>Heavy-Duty Cargo Net with Carabiner Hooks</strong> provides secure, reliable containment for loads on trucks, trailers, ATVs, and pickup beds. Hand-woven from high-tenacity polyester cord with a uniform diamond mesh, the net distributes load forces evenly. Four heavy-gauge stainless steel carabiner hooks enable fast, tool-free attachment to anchor rails and rings.</p>",
        "features": "High-tenacity polyester diamond mesh weave\nReinforced border rope for maximum perimeter strength\n4x stainless steel carabiner hooks at corners\nUV, moisture, and road grime resistant\nElastic design stretches for varied load sizes\nSuitable for trucks, trailers, ATVs, pickups\nMultiple size options: 1m x 1m to 3m x 4m"
    },
    {
        "name": "Flat Elastic Cargo Net – 6-Hook Universal 59",
        "desc": "<p>The <strong>Flat Elastic Cargo Net – 6-Hook Universal</strong> uses a flat grid of elastic bungee cords with 6 hook attachment points for secure, flexible load retention on motorcycles, bicycles, scooters, and small trailers. The flat design lies flush over luggage and cargo, providing 360-degree retention without bunching or rolling away from the load.</p>",
        "features": "Flat elastic bungee cord grid design\n6 hook attachment points for secure retention\nFlush, 360-degree cargo retention\nIdeal for motorcycles, bicycles, and scooters\nWeather resistant and UV stabilized\nOne-size-fits-most design stretches to fit\nSet of 2 nets included"
    },
    {
        "name": "Tubular Cargo Hammock Safety Net 60",
        "desc": "<p>The <strong>Tubular Cargo Hammock Safety Net</strong> is designed for overhead cargo retention in vans, trucks, and RVs. Suspended from the vehicle ceiling, it provides a large, flexible storage hammock for lightweight items such as sleeping bags, bedding, camping gear, and soft luggage. The tubular border rope distributes load stress evenly around the perimeter for maximum durability.</p>",
        "features": "Overhead suspension design for van/truck/RV use\nTubular border rope for perimeter load distribution\nHigh-tenacity polyester cord, open diamond mesh\nFits most standard van interiors\nMaximum load: 25 kg (lightweight items)\nIncludes stainless steel carabiner clips\nEasy installation with no drilling required"
    },
    {
        "name": "Fall Protection Safety Net – Industrial Grade 61",
        "desc": "<p>The <strong>Fall Protection Safety Net – Industrial Grade</strong> meets the requirements of EN1263 for personnel fall arrest at construction sites. Designed to be rigged below working platforms, scaffold edges, and open stairwells, it arrests the fall of a worker or falling object and absorbs the energy without damaging rebound. Includes all rigging hardware and border ropes.</p>",
        "features": "EN1263-1 personnel fall arrest certification\nHigh-tenacity polyamide mesh\nAbsorbs fall energy without rebound\nIncludes all rigging hardware and border ropes\nFire-retardant treatment available\nInstall under platforms, scaffold edges, stairwells\nFull inspection and certification service available"
    },
    {
        "name": "Construction Debris Safety Net 62",
        "desc": "<p>The <strong>Construction Debris Safety Net</strong> is designed for installation on scaffolding facades to catch falling tools, materials, and debris, protecting workers at lower levels and the public below. The fine woven polyethylene mesh retains all but the smallest objects and complies with BS 8411 and EN 1263 for scaffold debris net applications.</p>",
        "features": "Fine polyethylene mesh retains falling debris\nComplies with BS 8411 and EN 1263\nHigh-visibility color for site safety compliance\nResistant to UV, rain, and wind\nEasy installation with integrated border rope\nFlame-retardant compound option available\nSuitable for all scaffold and hoist tower applications"
    },
    {
        "name": "Knotted Polypropylene Sports & Playground Net 63",
        "desc": "<p>The <strong>Knotted Polypropylene Sports & Playground Net</strong> is manufactured from high-strength polypropylene twine with all knots heat-sealed for permanence and consistency. Used in sports halls, adventure playgrounds, climbing frames, and sports goal nets, it provides a durable, weather-resistant netting solution for high-impact recreational environments.</p>",
        "features": "High-strength polypropylene twine construction\nAll knots heat-sealed for permanence\nSuitable for sports halls and adventure playgrounds\nWeather resistant for outdoor installation\nAvailable in various mesh sizes and colors\nCustom dimensions available\nIdeal for climbing frames, goal nets, and dividers"
    },
    # ─── ACCESSORIES & TOOLS (64–70) ─────────────────────────
    {
        "name": "Heavy-Duty Canvas Ladder Tool & Accessory Bag 64",
        "desc": "<p>Our <strong>Heavy-Duty Canvas Ladder Tool Bag</strong> is designed to hang directly from any ladder rung using heavy-duty buckle straps, keeping your tools safely within reach at height. Built from rugged 600D Oxford canvas with reinforced double-stitching at all stress points, it features a wide-mouth opening and multiple internal pockets for organized tool access on the job.</p>",
        "features": "Rugged 600D Oxford canvas, double-reinforced stitching\nWide-mouth opening for easy tool access\nHeavy-duty buckle straps for ladder rung hanging\nMultiple internal and external storage pockets\nDurable metal zipper closures\nPadded carrying handle for transport\nDimensions: approx. 45cm x 25cm x 30cm"
    },
    {
        "name": "Low-Profile Silent TPR Furniture Caster Wheel Set 65",
        "desc": "<p>Our <strong>Low-Profile Silent TPR Furniture Caster Wheel Set</strong> is engineered for kick-plate and base-mounted furniture applications. The twin-wheel low-profile design provides exceptional stability under furniture bases while the thermoplastic rubber (TPR) wheels roll silently and leave zero marks on hardwood, laminate, tile, and marble floors.</p>",
        "features": "Twin-wheel low-profile design for furniture bases\nSilent-rolling TPR wheels — no floor marks\nPrecision ball-bearing 360° swivel bracket\nTop plate and stem mount options included\nRated load: 50 kg per caster\nWheel diameter: 38mm; Height: 45mm\nSilent and scratch-resistant compound"
    },
    {
        "name": "Heavy-Duty Locking Swivel Caster Wheels – Industrial 66",
        "desc": "<p>The <strong>Heavy-Duty Locking Swivel Caster Wheels</strong> are designed for industrial trolleys, workbench bases, and heavy equipment stands that must be easily repositioned and then locked firmly in place. The dual-action brake locks both the wheel rotation and the swivel plate simultaneously, ensuring absolute stability when locked.</p>",
        "features": "Dual-action brake locks wheel and swivel simultaneously\nHeavy-duty pressed steel swivel bracket\nSolid rubber or polyurethane wheel options\nRated load: 200 kg per caster\nWheel diameter: 100mm\nStem and top plate mounting options\nIdeal for industrial trolleys and workbenches"
    },
    {
        "name": "Polyester Binding Webbing Strip – Packing & Strapping 67",
        "desc": "<p>Our <strong>Polyester Binding Webbing Strip</strong> is the industrial standard for securing pallets, bales, and boxed cargo for transport. Woven from high-tenacity polyester yarns to a precise width and tensile specification, it integrates perfectly with standard metal and plastic buckle tensioners. Available in natural white and a range of standard colors for color-coded load identification.</p>",
        "features": "High-tenacity polyester, standard 19mm width\nNatural white and standard color options available\nBreak strength: 700 kg per 19mm width\nColor-coded options for load identification\nCompatible with standard metal and plastic buckles\nAvailable on 200m and 500m spools\nIdeal for pallet and bale securing"
    },
    {
        "name": "Aluminium Telescopic Pole – Reach Extension Tool 68",
        "desc": "<p>The <strong>Aluminium Telescopic Reach Extension Pole</strong> works with standard tool adapters to extend the reach of paint rollers, squeegees, window cleaners, and fruit pickers without the need for a ladder. Multiple twist-lock sections extend the pole to 6 meters while the compact collapsed length of 1.2 meters makes it manageable for transport and storage.</p>",
        "features": "Multi-section twist-lock extension to 6 meters\nCollapsed length: 1.2 meters for easy transport\nUniversal threaded adapter for standard tools\nLightweight aluminum construction\nFoam grip handle for comfortable extended use\nCompatible with paint rollers, squeegees, and mops\nMaximum load at full extension: 5 kg"
    },
    {
        "name": "Professional Scaffold Plank – Aluminium Hatch Platform 69",
        "desc": "<p>The <strong>Aluminium Scaffold Plank</strong> is a lightweight, high-strength work platform designed for use between scaffold frames, combination ladder legs, and trestle bases. Extruded from 6061-T6 aluminum with a ribbed anti-slip top surface, it provides a firm, non-flex working platform that is dramatically lighter than traditional timber scaffold boards.</p>",
        "features": "6061-T6 aluminum extrusion, ribbed anti-slip surface\nDramatically lighter than timber scaffold boards\nFits standard scaffold frames and trestle bases\nZero flex under rated load\nRated for 150 kg per running metre\nAvailable in 1m, 1.5m, 2m, and 2.5m lengths\nAnodized finish for weather resistance"
    },
    {
        "name": "Round Wire Sunshade Net – Greenhouse Shade Cloth 70",
        "desc": "<p>Our <strong>Round Wire Sunshade Net</strong> is manufactured using advanced round-wire knitting technology for superior structural integrity and dimensional stability compared to flat-tape shade cloth. Ideal for large commercial greenhouse installations, nurseries, and agricultural shading, it provides consistent shade percentage across the full width with zero sagging even in heavy rain and wind.</p>",
        "features": "Advanced round-wire knitting for dimensional stability\nZero sagging under rain and wind load\nConsistent shade percentage across full width\nAvailable in 30%, 50%, 70%, 80%, and 90% shade\nHeavy-duty UV-stabilized HDPE construction\nCustom widths from 1m to 12m\nIdeal for large commercial greenhouse installations"
    },
]

IMAGE_DIR = r"c:\Users\MD.MUNNA\Desktop\UK_portfolio\project\hardwork"


def get_all_images():
    """Get all images sorted, excluding duplicates (files with '(1)' in name)."""
    all_imgs = sorted([
        f for f in os.listdir(IMAGE_DIR)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        and '(1)' not in f
    ])
    return all_imgs


def distribute_images(all_images, num_products):
    """
    Distribute images across products evenly.
    Returns list of (main_image, [additional_images]) tuples.
    """
    total = len(all_images)
    base = total // num_products
    remainder = total % num_products

    distribution = []
    idx = 0
    for i in range(num_products):
        # Extra image for first 'remainder' products
        count = base + (1 if i < remainder else 0)
        chunk = all_images[idx: idx + count]
        idx += count
        if chunk:
            main = chunk[0]
            additional = chunk[1:]
        else:
            main = all_images[0]
            additional = []
        distribution.append((main, additional))
    return distribution


def seed_hardware_70():
    print("=" * 60)
    print("HARDWARE CATEGORY SEEDER — 70 PRODUCTS")
    print("=" * 60)

    # Delete existing hardware category
    existing = Category.objects.filter(slug='hardware-ladders-accessories')
    if existing.exists():
        print("Deleting existing 'Hardware, Ladders & Accessories' category...")
        existing.delete()

    # Create category
    category = Category.objects.create(
        name="Hardware, Ladders & Accessories",
        slug="hardware-ladders-accessories",
        hero_text=(
            "Premium quality aluminium ladders, heavy-duty hardware components, "
            "cargo straps, safety ropes, cargo nets, and industrial accessories. "
            "Manufactured to the highest international safety standards by Tianjin Tipei Hardware."
        ),
        is_active=True,
        order=10
    )
    print(f"Created category: {category.name}")

    all_images = get_all_images()
    total_images = len(all_images)
    num_products = len(HARDWARE_PRODUCTS_70)
    print(f"Total images: {total_images}")
    print(f"Total products: {num_products}")
    print(f"Avg images/product: {total_images / num_products:.1f}")
    print()

    # Distribute all images across 70 products
    distribution = distribute_images(all_images, num_products)

    created_count = 0
    total_additional = 0

    for i, (product_data, (main_img, additional_imgs)) in enumerate(
            zip(HARDWARE_PRODUCTS_70, distribution)):

        slug = slugify(product_data["name"])

        # Create product
        product = Product.objects.create(
            category=category,
            name=product_data["name"],
            slug=slug,
            description=product_data["desc"],
            features=product_data["features"],
            is_active=True,
            order=i + 1
        )

        # Set main image
        main_img_path = os.path.join(IMAGE_DIR, main_img)
        with open(main_img_path, 'rb') as f:
            product.main_image.save(main_img, File(f), save=True)

        # Set additional images
        add_count = 0
        for order_idx, add_img in enumerate(additional_imgs):
            add_img_path = os.path.join(IMAGE_DIR, add_img)
            if not os.path.exists(add_img_path):
                continue
            with open(add_img_path, 'rb') as f:
                pi = ProductImage(product=product, order=order_idx)
                pi.image.save(add_img, File(f), save=True)
            add_count += 1

        total_additional += add_count
        created_count += 1

        print(f"  [{i+1:2d}/{num_products}] {product_data['name']}")
        print(f"         Main: {main_img} | Additional: {add_count}")

    print()
    print("=" * 60)
    print(f"DONE! Category: 'Hardware, Ladders & Accessories'")
    print(f"Products created : {created_count}")
    print(f"Images used (main): {created_count}")
    print(f"Images used (extra): {total_additional}")
    print(f"Total images used  : {created_count + total_additional}")
    print("=" * 60)


if __name__ == "__main__":
    seed_hardware_70()
