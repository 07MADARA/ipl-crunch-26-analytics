from fpdf import FPDF
import os

class DarkDeck(FPDF):
    def header(self):
        # Background: #121212 (Landscape A4: 297 x 210)
        self.set_fill_color(18, 18, 18)
        self.rect(0, 0, 297, 210, 'F')
        
        self.set_y(10)
        self.set_font("helvetica", "B", 10)
        self.set_text_color(29, 185, 84) # Green accent
        self.cell(0, 10, "IPL CRUNCH '26 Analytics Submission", border=0, align="R")
        self.ln(15)

    def add_title_slide(self):
        self.add_page()
        self.set_y(80)
        self.set_font("helvetica", "B", 36)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, "Beyond the Eye Test: Engineering Truth in the IPL", align="C", new_x="LMARGIN", new_y="NEXT")
        
        self.set_font("helvetica", "I", 18)
        self.set_text_color(29, 185, 84)
        self.cell(0, 15, "Winning with Data, Not Just Opinions", align="C", new_x="LMARGIN", new_y="NEXT")
        
        self.set_y(140)
        self.set_font("helvetica", "", 14)
        self.set_text_color(200, 200, 200)
        self.multi_cell(0, 8, "- Every fan has an opinion; we brought the math.\n- Analyzed 1,200+ matches and 290,000+ deliveries.\n- Engineered advanced match-state metrics to quantify pressure and phase impact.\n- The Bottom Line: Conventional IPL wisdom is actively losing teams matches.", align="C")

    def add_content_slide(self, title, bullets, image_path=None):
        self.add_page()
        self.set_y(30)
        self.set_font("helvetica", "B", 24)
        self.set_text_color(255, 255, 255)
        self.multi_cell(0, 12, title, align="L")
        self.ln(10)
        
        self.set_font("helvetica", "", 14)
        self.set_text_color(220, 220, 220)
        
        # If there's an image, we split the slide
        if image_path and os.path.exists(image_path):
            # Text on the left, Image on the right
            self.set_x(15)
            for b in bullets:
                self.multi_cell(110, 8, f"- {b}")
                self.ln(4)
                
            # Place image
            self.image(image_path, x=135, y=45, w=150)
        else:
            self.set_x(15)
            for b in bullets:
                self.multi_cell(0, 8, f"- {b}")
                self.ln(5)

def build_pdf():
    pdf = DarkDeck(orientation="L", unit="mm", format="A4")
    
    # Slide 1
    pdf.add_title_slide()
    
    # Slide 2
    pdf.add_content_slide(
        "The Analytics Engine: Raw JSON to Actionable Intelligence",
        [
            "Zero Human Error: Automated end-to-end Python pipeline.",
            "Massive Scale: Ingested and parsed 1,200+ official Cricsheet JSON files into a highly optimized Parquet architecture.",
            "Custom Feature Engineering:",
            "  - Match Phase Impact: Granular tracking of Powerplay, Middle, and Death overs.",
            "  - Dot Ball Pressure Index: A proprietary rolling calculation of consecutive dot balls faced by a batter to measure in-game suffocation."
        ]
    )
    
    # Slide 3
    pdf.add_content_slide(
        "Where the Game is Won: Quantifying Match Phases",
        [
            "Not all runs are created equal.",
            "Evaluated run differentials across the Powerplay (0-5), Middle (6-14), and Death (15-19) overs.",
            "Mapped phase-specific performance directly against the final margin of victory.",
            "Visualized the true correlation between phase dominance and match outcome."
        ],
        r"e:\ipl crunch\output_visuals\phase_impact_margin.png"
    )
    
    # Slide 4
    pdf.add_content_slide(
        "The Surprise Insight: The Dubai Trap",
        [
            "The Global Standard: Across the IPL, teams choosing to chase win 53.8% of the time.",
            "The Anomaly: At the Dubai International Cricket Stadium, teams choosing to chase win only 40.7% of the time.",
            "The Trap: Captains following the default T20 chasing meta in Dubai are statistically handicapping their own teams."
        ],
        r"e:\ipl crunch\output_visuals\toss_impact_by_venue.png"
    )
    
    # Slide 5
    pdf.add_content_slide(
        "Data Wins Tournaments",
        [
            "Intuition gets you to the IPL; Analytics wins you the trophy.",
            "Our pipeline turns raw unstructured data into a competitive edge.",
            "Exploiting anomalies (like the Dubai Trap) yields immediate win-probability gains.",
            "Next Steps: Integrate phase dynamics and pressure metrics into real-time auction and match-day strategy."
        ]
    )
    
    out_path = r"e:\ipl crunch\IPL_Crunch_26_Presentation.pdf"
    pdf.output(out_path)
    print(f"Presentation saved to {out_path}")

if __name__ == "__main__":
    build_pdf()
