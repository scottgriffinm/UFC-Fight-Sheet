#!/usr/bin/env python
"""Create an info sheet on all the UFC fights scheduled for today."""

"""
1. Check if there's a UFC event today, collect the event name
2. Get the list of fights
3. Get info on each fight, including:
    - Info on the fighters (from ESPN), including:
        - Betting odds
        - Height
        - Weight
        - Age
        - Reach
        - Stance
        - SIG STR LPM
        - SIG STR %
        - SIG STR ACC
        - TD AVG
        - TD ACC
        - SUB AVG
        - W-L-D
        - (T)KO Record
        - Submission Record
        - Last 5 fights
        - YouTube links of the last 5 fights for each fighter
4. Create a markdown file with the info for each fight, in chronological order
5. Save the file to the current directory


Agents:
ufc event search - checks if there's a UFC event today, and if so, returns the event name
fight info search - collects info on each fight, excluding video links
fight video link search - collects video links for each fight

*** we need to ensure that structured outputs are used to transfer info between agents to ensure that the info is consistent and accurate

"""

import argparse
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from llm.tasks import event_search, fight_info_search, video_link_search, test_llm


@dataclass
class Fighter:
    name: str
    betting_odds: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    age: Optional[int] = None
    reach: Optional[str] = None
    stance: Optional[str] = None
    sig_str_lpm: Optional[str] = None
    sig_str_percent: Optional[str] = None
    sig_str_acc: Optional[str] = None
    td_avg: Optional[str] = None
    td_acc: Optional[str] = None
    sub_avg: Optional[str] = None
    record: Optional[str] = None
    ko_record: Optional[str] = None
    submission_record: Optional[str] = None
    last_5_fights: Optional[List[str]] = None
    video_links: Optional[List[str]] = None


@dataclass
class Fight:
    event_name: str
    fight_number: int
    weight_class: str
    fighter1: Fighter
    fighter2: Fighter
    main_event: bool = False
    co_main_event: bool = False


async def get_ufc_event_info() -> Optional[str]:
    """Check if there's a UFC event today and return the event name."""
    print("🔍 [STEP 1] Checking for UFC events today...")
    today = datetime.now().strftime("%B %d, %Y")
    print(f"   📅 Today's date: {today}")
    try:
        print("   📡 Calling event search agent...")
        event_name = await event_search()
        if event_name:
            print(f"   ✅ Event found: {event_name}")
        else:
            print("   ❌ No events found for today")
        return event_name if event_name else None
    except Exception as e:
        print(f"   💥 Error checking for UFC events: {e}")
        return None


async def get_fight_info(event_name: str, limit: Optional[int] = None) -> List[Fight]:
    """Get detailed information about all fights in the event."""
    print(f"📊 [STEP 2] Collecting fight information for event: {event_name}")
    if limit:
        print(f"   🎯 Limiting to last {limit} fights")
    try:
        print("   📡 Calling fight info search agent...")
        fights_data = await fight_info_search(event_name)
        print(f"   📋 Received data for {len(fights_data)} fights")
        
        # Debug: Print the structure of the first fight
        if fights_data:
            print(f"   🔍 Debug - First fight structure: {fights_data[0]}")
        
        # Apply limit if specified (take last N fights)
        if limit and limit < len(fights_data):
            fights_data = fights_data[-limit:]
            print(f"   ✂️  Limited to last {limit} fights")
        
        fights = []
        for i, fight_data in enumerate(fights_data):
            print(f"   🔄 Processing fight {i + 1}/{len(fights_data)}...")
            
            # Extract fighter data with better error handling
            fighter1_data = fight_data.get("fighter1", {})
            fighter2_data = fight_data.get("fighter2", {})
            
            # Ensure fighter names exist
            fighter1_name = fighter1_data.get('name', 'Unknown Fighter 1')
            fighter2_name = fighter2_data.get('name', 'Unknown Fighter 2')
            
            print(f"      👊 Fighter 1: {fighter1_name}")
            print(f"      👊 Fighter 2: {fighter2_name}")
            
            # Create fighter objects with safe defaults
            try:
                fighter1 = Fighter(name=fighter1_name, **{k: v for k, v in fighter1_data.items() if k != 'name'})
                fighter2 = Fighter(name=fighter2_name, **{k: v for k, v in fighter2_data.items() if k != 'name'})
            except Exception as e:
                print(f"      💥 Error creating fighter objects: {e}")
                print(f"      🔧 Using fallback fighter data...")
                fighter1 = Fighter(name=fighter1_name)
                fighter2 = Fighter(name=fighter2_name)
            
            fight = Fight(
                event_name=event_name,
                fight_number=i + 1,
                weight_class=fight_data.get("weight_class", "Unknown"),
                fighter1=fighter1,
                fighter2=fighter2,
                main_event=fight_data.get("main_event", False),
                co_main_event=fight_data.get("co_main_event", False)
            )
            fights.append(fight)
            
            # Print fight details
            event_type = "🏆 MAIN EVENT" if fight.main_event else "🥈 CO-MAIN" if fight.co_main_event else "🥊 FIGHT"
            print(f"      {event_type} - {fight.weight_class}")
        
        print(f"   ✅ Successfully processed {len(fights)} fights")
        return fights
    except Exception as e:
        print(f"   💥 Error getting fight info: {e}")
        return []


async def get_video_links(fights: List[Fight]) -> List[Fight]:
    """Get YouTube video links for each fighter's recent fights."""
    print("🎥 [STEP 3] Collecting video links for each fighter...")
    total_fighters = len(fights) * 2
    current_fighter = 0
    
    for fight_idx, fight in enumerate(fights):
        print(f"   🥊 Processing fight {fight.fight_number}: {fight.fighter1.name} vs {fight.fighter2.name}")
        
        try:
            # Get video links for fighter 1
            current_fighter += 1
            print(f"      📹 [{current_fighter}/{total_fighters}] Searching videos for {fight.fighter1.name}...")
            fighter1_videos = await video_link_search(fight.fighter1.name)
            fight.fighter1.video_links = fighter1_videos
            print(f"         ✅ Found {len(fighter1_videos)} videos for {fight.fighter1.name}")
            
            # Get video links for fighter 2
            current_fighter += 1
            print(f"      📹 [{current_fighter}/{total_fighters}] Searching videos for {fight.fighter2.name}...")
            fighter2_videos = await video_link_search(fight.fighter2.name)
            fight.fighter2.video_links = fighter2_videos
            print(f"         ✅ Found {len(fighter2_videos)} videos for {fight.fighter2.name}")
            
        except Exception as e:
            print(f"      💥 Error getting video links for fight {fight.fight_number}: {e}")
            # Continue with other fights even if one fails
            continue
    
    print(f"   ✅ Video collection complete for {len(fights)} fights")
    return fights


def create_markdown_content(fights: List[Fight], limit: Optional[int] = None) -> str:
    """Create markdown content for the fight sheet."""
    print("📝 [STEP 4] Generating markdown content...")
    today = datetime.now().strftime("%B %d, %Y")
    
    print("   📄 Creating document header...")
    content = f"# UFC Fight Sheet - {today}\n\n"
    
    if not fights:
        print("   ⚠️  No fights to document")
        content += "No UFC events scheduled for today.\n"
        return content
    
    event_name = fights[0].event_name
    content += f"## Event: {event_name}\n\n"
    content += f"**Date:** {today}\n\n"
    if limit:
        content += f"**Fights Included:** Last {len(fights)} fights (limited from full event)\n\n"
    else:
        content += f"**Total Fights:** {len(fights)}\n\n"
    content += "---\n\n"
    
    print(f"   📋 Processing {len(fights)} fights for markdown...")
    for fight_idx, fight in enumerate(fights):
        print(f"      📄 Writing fight {fight_idx + 1}/{len(fights)}: {fight.fighter1.name} vs {fight.fighter2.name}")
        
        # Fight header
        if fight.main_event:
            content += f"### 🏆 MAIN EVENT - Fight #{fight.fight_number}\n\n"
        elif fight.co_main_event:
            content += f"### 🥈 CO-MAIN EVENT - Fight #{fight.fight_number}\n\n"
        else:
            content += f"### Fight #{fight.fight_number}\n\n"
        
        content += f"**Weight Class:** {fight.weight_class}\n\n"
        
        # Fighter comparison table
        content += "| Stat | Fighter 1 | Fighter 2 |\n"
        content += "|------|-----------|-----------|\n"
        content += f"| **Name** | {fight.fighter1.name} | {fight.fighter2.name} |\n"
        content += f"| **Record** | {fight.fighter1.record or 'N/A'} | {fight.fighter2.record or 'N/A'} |\n"
        content += f"| **Age** | {fight.fighter1.age or 'N/A'} | {fight.fighter2.age or 'N/A'} |\n"
        content += f"| **Height** | {fight.fighter1.height or 'N/A'} | {fight.fighter2.height or 'N/A'} |\n"
        content += f"| **Reach** | {fight.fighter1.reach or 'N/A'} | {fight.fighter2.reach or 'N/A'} |\n"
        content += f"| **Stance** | {fight.fighter1.stance or 'N/A'} | {fight.fighter2.stance or 'N/A'} |\n"
        content += f"| **Betting Odds** | {fight.fighter1.betting_odds or 'N/A'} | {fight.fighter2.betting_odds or 'N/A'} |\n\n"
        
        # Detailed stats
        content += "#### Striking Stats\n"
        content += "| Stat | Fighter 1 | Fighter 2 |\n"
        content += "|------|-----------|-----------|\n"
        content += f"| **Sig Str LPM** | {fight.fighter1.sig_str_lpm or 'N/A'} | {fight.fighter2.sig_str_lpm or 'N/A'} |\n"
        content += f"| **Sig Str %** | {fight.fighter1.sig_str_percent or 'N/A'} | {fight.fighter2.sig_str_percent or 'N/A'} |\n"
        content += f"| **Sig Str ACC** | {fight.fighter1.sig_str_acc or 'N/A'} | {fight.fighter2.sig_str_acc or 'N/A'} |\n\n"
        
        content += "#### Grappling Stats\n"
        content += "| Stat | Fighter 1 | Fighter 2 |\n"
        content += "|------|-----------|-----------|\n"
        content += f"| **TD AVG** | {fight.fighter1.td_avg or 'N/A'} | {fight.fighter2.td_avg or 'N/A'} |\n"
        content += f"| **TD ACC** | {fight.fighter1.td_acc or 'N/A'} | {fight.fighter2.td_acc or 'N/A'} |\n"
        content += f"| **SUB AVG** | {fight.fighter1.sub_avg or 'N/A'} | {fight.fighter2.sub_avg or 'N/A'} |\n\n"
        
        # Records
        content += "#### Records\n"
        content += "| Record Type | Fighter 1 | Fighter 2 |\n"
        content += "|-------------|-----------|-----------|\n"
        content += f"| **(T)KO** | {fight.fighter1.ko_record or 'N/A'} | {fight.fighter2.ko_record or 'N/A'} |\n"
        content += f"| **Submissions** | {fight.fighter1.submission_record or 'N/A'} | {fight.fighter2.submission_record or 'N/A'} |\n\n"
        
        # Last 5 fights
        content += "#### Last 5 Fights\n"
        content += f"**{fight.fighter1.name}:**\n"
        if fight.fighter1.last_5_fights:
            for i, result in enumerate(fight.fighter1.last_5_fights, 1):
                content += f"{i}. {result}\n"
        else:
            content += "N/A\n"
        
        content += f"\n**{fight.fighter2.name}:**\n"
        if fight.fighter2.last_5_fights:
            for i, result in enumerate(fight.fighter2.last_5_fights, 1):
                content += f"{i}. {result}\n"
        else:
            content += "N/A\n"
        
        # Video links
        content += "\n#### Recent Fight Videos\n"
        content += f"**{fight.fighter1.name}:**\n"
        if fight.fighter1.video_links:
            for i, link in enumerate(fight.fighter1.video_links, 1):
                content += f"{i}. [Fight Video {i}]({link})\n"
        else:
            content += "No videos available\n"
        
        content += f"\n**{fight.fighter2.name}:**\n"
        if fight.fighter2.video_links:
            for i, link in enumerate(fight.fighter2.video_links, 1):
                content += f"{i}. [Fight Video {i}]({link})\n"
        else:
            content += "No videos available\n"
        
        content += "\n---\n\n"
    
    print("   ✅ Markdown content generation complete")
    return content


async def main(limit: Optional[int] = None):
    """Main function to generate the UFC fight sheet."""
    print("🚀 Starting UFC Fight Sheet Generator")
    if limit:
        print(f"🎯 Limiting to last {limit} fights")
    print("=" * 50)
    
    # Step 1: Check for UFC events today
    event_name = await get_ufc_event_info()
    
    if not event_name:
        print("❌ No UFC events scheduled for today.")
        print("📝 Creating empty fight sheet...")
        content = create_markdown_content([], limit)
    else:
        print(f"✅ Found UFC event: {event_name}")
        
        # Step 2: Get fight information
        fights = await get_fight_info(event_name, limit)
        
        if not fights:
            print("❌ No fights found for this event.")
            print("📝 Creating empty fight sheet...")
            content = create_markdown_content([], limit)
        else:
            print(f"✅ Found {len(fights)} fights")
            
            # Step 3: Get video links
            fights = await get_video_links(fights)
            
            # Step 4: Create markdown content
            content = create_markdown_content(fights, limit)
    
    # Step 5: Save to file
    print("💾 [STEP 5] Saving fight sheet to file...")
    filename = f"ufc_fight_sheet_{datetime.now().strftime('%Y%m%d')}.md"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ Fight sheet saved successfully to: {filename}")
        
        # Print summary
        print("\n" + "=" * 50)
        print("🎉 UFC Fight Sheet Generation Complete!")
        print(f"📁 File: {filename}")
        if event_name:
            print(f"📅 Event: {event_name}")
            print(f"🥊 Fights: {len(fights) if 'fights' in locals() else 0}")
            if limit:
                print(f"🎯 Limited to last {limit} fights")
        print("=" * 50)
        
    except Exception as e:
        print(f"   💥 Error saving file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a UFC fight sheet for today.")
    parser.add_argument("--last-n-fights", type=int, default=None, help="Limit the number of fights to process (e.g., --last-n-fights 5).")
    args = parser.parse_args()

    asyncio.run(main(args.last_n_fights))

