
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class CellLineClone:
    """Represents a CHO cell clone producing a therapeutic antibody"""
    
    def __init__(self, clone_id, parent_line="CHO-K1"):
        self.id = clone_id
        self.parent = parent_line
        
       
        self.base_titer = random.gauss(2.5, 1.5)  
        self.growth_rate = random.gauss(0.032, 0.008)  
        self.viability = random.gauss(94, 6)  
        self.stability = random.choice([True, True, True, False])  
        
       
        self.glycosylation_pattern = random.choice(['Optimal', 'Optimal', 'Good', 'Poor'])
        self.aggregation_level = random.uniform(0.5, 8.0)  
        
       
        self.base_titer = max(0.1, min(6.0, self.base_titer))
        self.viability = max(60, min(99, self.viability))
        self.growth_rate = max(0.015, min(0.050, self.growth_rate))
        
       
        self.day0_density = 0.5e6  
        self.day3_density = None
        self.day7_density = None
        self.day7_viability = None
        self.day7_titer = None
    
    def grow(self, days):
        """Simulate cell growth over time"""
        
        time_hours = days * 24
        peak_density = 8e6  
        
        density = self.day0_density * np.exp(self.growth_rate * time_hours)
        density = min(density, peak_density)  
        
       
        viability = self.viability - (days * 0.5)
        viability = max(60, viability)
        
        return density, viability
    
    def produce_antibody(self, days):
        """Calculate antibody production (titer)"""
        
        density, viability = self.grow(days)
        
       
        qP = self.base_titer * 10  
        
       
        titer = (self.base_titer * days / 7) * (viability / 100)
        
       
        titer = titer * random.gauss(1.0, 0.1)
        
        return max(0.1, titer)
    
    def score(self):
        """Calculate overall quality score for ranking"""
       
        titer_score = min(1.0, self.day7_titer / 5.0) if self.day7_titer else 0
        viability_score = (self.day7_viability / 100) if self.day7_viability else 0
        growth_score = min(1.0, self.growth_rate / 0.045)
        stability_bonus = 0.2 if self.stability else 0
        quality_bonus = 0.15 if self.glycosylation_pattern == 'Optimal' else 0
        quality_penalty = -0.1 if self.aggregation_level > 5.0 else 0
        
        total_score = (
            titer_score * 0.40 +     
            viability_score * 0.25 +  
            growth_score * 0.10 +     
            stability_bonus +         
            quality_bonus +           
            quality_penalty           
        )
        
        return round(total_score, 3)


class AutomatedScreening:
    """Simulates automated high-throughput cell line screening"""
    
    def __init__(self, num_clones=96, plate_format='96-well'):
        self.num_clones = num_clones
        self.plate_format = plate_format
        self.clones = [CellLineClone(f"Clone_{i+1:03d}") for i in range(num_clones)]
        self.screening_log = []
        self.start_date = datetime.now()
    
    def day_0_seed_plates(self):
        """Day 0: Robot seeds cells into plates"""
        print("\n" + "=" * 80)
        print("DAY 0: SEEDING CELLS")
        print("=" * 80)
        print(f"Date: {self.start_date.strftime('%Y-%m-%d')}")
        print(f"\n🔬 Screening {self.num_clones} CHO cell clones for antibody production")
        print(f"📋 Plate format: {self.plate_format}")
        print(f"🤖 Automated liquid handling system: Hamilton STAR")
        
        print("\n⚙️  Protocol Steps:")
        print("  1. Thaw cryopreserved clones from -80°C")
        print("  2. Count viable cells (Vi-CELL analyzer)")
        print("  3. Dilute to 0.5 × 10⁶ cells/mL")
        print("  4. Robot dispenses 200 µL per well")
        print("  5. Add basal media + 4 mM glutamine")
        
        for clone in self.clones:
            self.screening_log.append({
                'day': 0,
                'clone_id': clone.id,
                'action': 'seeded',
                'volume_ul': 200,
                'density_cells_ml': clone.day0_density
            })
        
        print(f"\n✅ {len(self.clones)} clones seeded successfully")
        print(f"   Initial density: {self.clones[0].day0_density:.1e} cells/mL")
        print(f"   Media: CD CHO (chemically defined)")
        print(f"   Conditions: 37°C, 5% CO₂, 125 rpm shaking")
    
    def day_3_feed_and_sample(self):
        """Day 3: Robot adds feed and takes samples"""
        print("\n" + "=" * 80)
        print("DAY 3: FEEDING & SAMPLING")
        print("=" * 80)
        
        day3_date = self.start_date + timedelta(days=3)
        print(f"Date: {day3_date.strftime('%Y-%m-%d')}")
        
        print("\n⚙️  Protocol Steps:")
        print("  1. Robot samples 50 µL from each well")
        print("  2. Measure cell density & viability (Vi-CELL)")
        print("  3. Add 50 µL feed media (glucose + amino acids)")
        print("  4. Store samples at -80°C for later titer analysis")
        
        for clone in self.clones:
            density, viability = clone.grow(days=3)
            clone.day3_density = density
            
            self.screening_log.append({
                'day': 3,
                'clone_id': clone.id,
                'action': 'fed_and_sampled',
                'feed_volume_ul': 50,
                'sample_volume_ul': 50,
                'density': density,
                'viability': viability
            })
        
        avg_density = np.mean([c.day3_density for c in self.clones])
        print(f"\n✅ All {len(self.clones)} wells processed")
        print(f"   Average density: {avg_density:.2e} cells/mL")
        print(f"   Expected: 2-4 × 10⁶ cells/mL (healthy growth)")
    
    def day_7_harvest_and_analyze(self):
        """Day 7: Final harvest and comprehensive analysis"""
        print("\n" + "=" * 80)
        print("DAY 7: HARVEST & ANALYSIS")
        print("=" * 80)
        
        day7_date = self.start_date + timedelta(days=7)
        print(f"Date: {day7_date.strftime('%Y-%m-%d')}")
        
        print("\n⚙️  Protocol Steps:")
        print("  1. Robot harvests all wells (full volume)")
        print("  2. Centrifuge to separate cells from supernatant")
        print("  3. Measure final cell density & viability")
        print("  4. Measure antibody titer (ELISA or Octet)")
        print("  5. Optional: LC-MS for product quality analysis")
        
        
        results = []
        for clone in self.clones:
            density, viability = clone.grow(days=7)
            titer = clone.produce_antibody(days=7)
            
            clone.day7_density = density
            clone.day7_viability = viability
            clone.day7_titer = titer
            
            results.append({
                'Clone ID': clone.id,
                'Titer (g/L)': round(titer, 2),
                'Viability (%)': round(viability, 1),
                'VCD (10⁶ cells/mL)': round(density / 1e6, 2),
                'Growth Rate': round(clone.growth_rate, 4),
                'Stable': 'Yes' if clone.stability else 'No',
                'Glycosylation': clone.glycosylation_pattern,
                'Aggregates (%)': round(clone.aggregation_level, 1),
                'Score': clone.score()
            })
        
        df = pd.DataFrame(results)
        
        print(f"\n✅ Analysis complete for all {len(self.clones)} clones")
        print(f"\n📊 SCREENING STATISTICS:")
        print(f"   Mean Titer: {df['Titer (g/L)'].mean():.2f} g/L")
        print(f"   Max Titer: {df['Titer (g/L)'].max():.2f} g/L")
        print(f"   Mean Viability: {df['Viability (%)'].mean():.1f}%")
        print(f"   High Producers (>3 g/L): {(df['Titer (g/L)'] > 3).sum()} clones")
        print(f"   Stable Clones: {(df['Stable'] == 'Yes').sum()}/{len(df)}")
        
        return df
    
    def select_top_clones(self, df, n=10):
        """Select top performing clones for advancement"""
        print("\n" + "=" * 80)
        print(f"🏆 TOP {n} CLONE SELECTION")
        print("=" * 80)
        
      
        top_clones = df.nlargest(n, 'Score')
        
        print("\n📋 Selection Criteria:")
        print("   • High titer (>2.5 g/L preferred)")
        print("   • High viability (>85%)")
        print("   • Stable expression")
        print("   • Good product quality (low aggregation)")
        print("   • Optimal glycosylation pattern")
        
        print(f"\n🎯 SELECTED CLONES:\n")
        print(top_clones.to_string(index=False))
        
        print(f"\n✅ {n} clones selected for scale-up to shake flasks")
        print("   Next steps:")
        print("   1. Expand in 125 mL shake flasks")
        print("   2. Validate titer in fed-batch (14 days)")
        print("   3. Assess stability over 60 generations")
        print("   4. Best clone → Scale to bioreactor (2L → 200L → 2000L)")
        
        return top_clones
    
    def run_full_screening_campaign(self):
        """Execute complete 7-day screening protocol"""
        print("\n" + "=" * 80)
        print("🧬 AUTOMATED CELL LINE SCREENING CAMPAIGN")
        print("   Johnson & Johnson - Cell Engineering & Analytical Sciences")
        print("=" * 80)
        print(f"Campaign Start: {self.start_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Clones to Screen: {self.num_clones}")
        print(f"Objective: Identify high-titer, stable antibody producers")
        print("=" * 80)
        
       
        self.day_0_seed_plates()
        
        
        self.day_3_feed_and_sample()
        
       
        results_df = self.day_7_harvest_and_analyze()
        
       
        top_clones = self.select_top_clones(results_df, n=10)
        
       
        end_time = datetime.now()
        
        print("\n" + "=" * 80)
        print("📈 CAMPAIGN SUMMARY")
        print("=" * 80)
        print(f"Campaign End: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Clones Screened: {self.num_clones}")
        print(f"Clones Advanced: {len(top_clones)}")
        print(f"Success Rate: {len(top_clones)/self.num_clones*100:.1f}%")
        print(f"Best Titer: {results_df['Titer (g/L)'].max():.2f} g/L")
        print(f"Best Clone: {results_df.loc[results_df['Score'].idxmax(), 'Clone ID']}")
        
       
        filename = f"screening_results_{self.start_date.strftime('%Y%m%d')}.csv"
        results_df.to_csv(filename, index=False)
        print(f"\n💾 Results saved to: {filename}")
        
        print("\n" + "=" * 80)
        print("🎓 KEY CONCEPTS DEMONSTRATED:")
        print("=" * 80)
        print("✅ CHO cell line development workflow")
        print("✅ High-throughput automated screening")
        print("✅ Titer, viability, and growth metrics")
        print("✅ Multi-criteria clone selection")
        print("✅ Product quality assessment")
        print("✅ Why automation is critical (96+ clones manually = impossible!)")
        print("\n💡 This is EXACTLY what you'll support at J&J!")
        print("   Your automation systems enable scientists to screen")
        print("   THOUSANDS of clones to find the best antibody producers!")
        print("=" * 80 + "\n")
        
        return results_df, top_clones


def main():
    """Run the cell line screening simulation"""
    
    print("\n" + "=" * 80)
    print("🧬 CELL LINE DEVELOPMENT SIMULATOR")
    print("   Teaching biotherapeutic production for J&J co-op")
    print("=" * 80)
    
    print("\n📚 BACKGROUND:")
    print("   Biotherapeutics (antibodies, proteins) are made by living cells")
    print("   CHO cells (Chinese Hamster Ovary) are the industry workhorse")
    print("   Must screen 100s-1000s of clones to find best producers")
    print("   Manual screening: IMPOSSIBLE at scale")
    print("   Automated screening: Enables industry-scale production")
    
    input("\n⏸️  Press Enter to start screening campaign...")
    
   
    screening = AutomatedScreening(num_clones=96)
    results_df, top_clones = screening.run_full_screening_campaign()
    
  
    print("\n" + "=" * 80)
    print("⏱️  TIME COMPARISON:")
    print("=" * 80)
    print("Manual screening (1 person, 96 clones):")
    print("   Day 0: ~8 hours (seeding, counting, diluting)")
    print("   Day 3: ~6 hours (sampling, feeding, analysis)")
    print("   Day 7: ~10 hours (harvest, centrifuge, assays)")
    print("   Total: ~24 hours of intensive pipetting")
    print("   Error rate: HIGH (fatigue, inconsistency)")
    print("\nAutomated screening (Hamilton STAR):")
    print("   Day 0: ~45 minutes (robot does everything)")
    print("   Day 3: ~30 minutes")
    print("   Day 7: ~1 hour")
    print("   Total: ~2 hours of setup/monitoring")
    print("   Error rate: MINIMAL (precise, reproducible)")
    print("\n💡 Automation = 12x faster + more reliable!")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()