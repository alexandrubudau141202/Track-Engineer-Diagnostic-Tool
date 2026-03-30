"""
PDF Generator
Creates professional GT3 R diagnostic reports with embedded graphs and recommendations.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image as RLImage
)
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend

from app.models.diagnosis import DiagnosisResult
from app.models.telemetry import ProcessedTelemetry


class PDFGenerator:
    """Generate professional diagnosis reports as PDF"""
    
    def __init__(self, diagnosis: DiagnosisResult, telemetry: ProcessedTelemetry):
        self.diagnosis = diagnosis
        self.telemetry = telemetry
        self.styles = getSampleStyleSheet()
        self._define_custom_styles()
    
    def _define_custom_styles(self):
        """Define custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1f4788'),
            spaceAfter=20,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='ProblemHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#c41e3a'),
            spaceAfter=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='RecommendationText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8
        ))
    
    def generate(self, filename: str = "report.pdf") -> str:
        """Generate PDF report"""
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        elements = []
        
        # Title page
        elements.extend(self._build_title_page())
        elements.append(PageBreak())
        
        # Executive Summary
        elements.extend(self._build_executive_summary())
        elements.append(Spacer(1, 0.3*inch))
        
        # Telemetry Analysis (with graphs)
        elements.extend(self._build_telemetry_section())
        elements.append(PageBreak())
        
        # Problem Diagnosis
        elements.extend(self._build_diagnosis_section())
        elements.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        elements.extend(self._build_recommendations_section())
        elements.append(Spacer(1, 0.2*inch))
        
        # Driver Coaching (if available)
        if self.diagnosis.driver_coaching:
            elements.extend(self._build_coaching_section())
            elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        elements.extend(self._build_footer())
        
        # Build PDF
        doc.build(elements)
        return filename
    
    # ========== TITLE PAGE ==========
    def _build_title_page(self) -> list:
        """Build title page"""
        elements = []
        
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("GT3 R TRACK DIAGNOSIS REPORT", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Scenario info
        info_data = [
            ["Scenario ID:", self.diagnosis.scenario_id],
            ["Report Date:", datetime.now().strftime("%Y-%m-%d %H:%M UTC")],
            ["Primary Issue:", f"<b>{self.diagnosis.primary_problem}</b>"],
            ["Overall Confidence:", f"{self.diagnosis.overall_confidence_percent}%"],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(info_table)
        return elements
    
    # ========== EXECUTIVE SUMMARY ==========
    def _build_executive_summary(self) -> list:
        """Build executive summary section"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Summary text
        if self.diagnosis.summary:
            elements.append(Paragraph(self.diagnosis.summary, self.styles['Normal']))
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Problems detected (bulleted)
        if self.diagnosis.problems_detected:
            elements.append(Paragraph("<b>Issues Identified:</b>", self.styles['Normal']))
            for problem in self.diagnosis.problems_detected[:3]:
                severity_color = {'high': '#c41e3a', 'medium': '#ff8c00', 'low': '#4CAF50'}
                color = severity_color.get(problem.severity, '#000000')
                elements.append(Paragraph(
                    f"• <font color='{color}'>{problem.type.replace('_', ' ').title()}</font> "
                    f"({problem.severity}, {problem.confidence_percent}% confidence)",
                    self.styles['Normal']
                ))
        
        return elements
    
    # ========== TELEMETRY SECTION ==========
    def _build_telemetry_section(self) -> list:
        """Build telemetry analysis section with graphs"""
        elements = []
        
        elements.append(Paragraph("TELEMETRY ANALYSIS", self.styles['Heading2']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Key metrics table
        metrics = self.telemetry.metrics
        metrics_data = [
            ["Speed (km/h)", f"Avg: {metrics.avg_speed_kmh:.1f} | Max: {metrics.max_speed_kmh:.1f}"],
            ["Lateral G", f"Max: {metrics.max_lateral_g:.2f}G | Avg: {metrics.avg_lateral_g:.2f}G"],
            ["Steering", f"Avg: {metrics.avg_steering_angle_deg:.1f}° | Max: {metrics.max_steering_angle_deg:.1f}°"],
            ["Braking", f"Max Pressure: {metrics.max_brake_pressure_bar:.1f} bar"],
        ]
        
        # Add tire temps if available
        if metrics.avg_tire_temp_c:
            fl = metrics.avg_tire_temp_c.get("fl", 0)
            fr = metrics.avg_tire_temp_c.get("fr", 0)
            rl = metrics.avg_tire_temp_c.get("rl", 0)
            rr = metrics.avg_tire_temp_c.get("rr", 0)
            metrics_data.append([
                "Tire Temps (°C)",
                f"FL: {fl:.0f} | FR: {fr:.0f} | RL: {rl:.0f} | RR: {rr:.0f}"
            ])
        
        metrics_table = Table(metrics_data, colWidths=[2*inch, 3.5*inch])
        metrics_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white, HexColor('#f0f0f0')]),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Graphs
        graph_path = self._generate_telemetry_graphs()
        if graph_path:
            try:
                img = RLImage(graph_path, width=6.5*inch, height=4*inch)
                elements.append(img)
            except Exception:
                pass  # Graph generation failed, skip
        
        return elements
    
    def _generate_telemetry_graphs(self) -> str:
        """Generate telemetry visualization graphs"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(10, 8))
            fig.suptitle('Telemetry Metrics Summary', fontsize=14, fontweight='bold')
            
            metrics = self.telemetry.metrics
            
            # Speed distribution
            ax = axes[0, 0]
            ax.bar(['Min', 'Avg', 'Max'], 
                   [metrics.min_speed_kmh, metrics.avg_speed_kmh, metrics.max_speed_kmh],
                   color=['#4CAF50', '#2196F3', '#FF9800'])
            ax.set_ylabel('Speed (km/h)')
            ax.set_title('Speed Profile')
            ax.grid(axis='y', alpha=0.3)
            
            # Tire temperatures
            ax = axes[0, 1]
            if metrics.avg_tire_temp_c:
                temps = [
                    metrics.avg_tire_temp_c.get("fl", 0),
                    metrics.avg_tire_temp_c.get("fr", 0),
                    metrics.avg_tire_temp_c.get("rl", 0),
                    metrics.avg_tire_temp_c.get("rr", 0),
                ]
                ax.bar(['FL', 'FR', 'RL', 'RR'], temps, color=['#FF5252', '#FF5252', '#FF9800', '#FF9800'])
                ax.set_ylabel('Temperature (°C)')
                ax.set_title('Tire Temperatures')
                ax.axhline(y=95, color='red', linestyle='--', linewidth=1, alpha=0.7, label='High Temp')
                ax.grid(axis='y', alpha=0.3)
                ax.legend()
            
            # G-forces
            ax = axes[1, 0]
            ax.bar(['Lateral', 'Longitudinal'], 
                   [metrics.max_lateral_g, metrics.max_longitudinal_g],
                   color=['#2196F3', '#4CAF50'])
            ax.set_ylabel('G-Force')
            ax.set_title('Peak G-Forces')
            ax.grid(axis='y', alpha=0.3)
            
            # Events
            ax = axes[1, 1]
            events = [metrics.understeer_events, metrics.oversteer_events, metrics.braking_inefficiency_events]
            ax.bar(['Understeer', 'Oversteer', 'Brake Issue'], events, 
                   color=['#FF6F00', '#FF5252', '#9C27B0'])
            ax.set_ylabel('Event Count')
            ax.set_title('Detected Events')
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            
            # Save to buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close(fig)
            
            # Save to temp file
            temp_path = "/tmp/telemetry_graph.png"
            with open(temp_path, 'wb') as f:
                f.write(img_buffer.getvalue())
            
            return temp_path
        except Exception as e:
            print(f"Graph generation error: {e}")
            return None
    
    # ========== DIAGNOSIS SECTION ==========
    def _build_diagnosis_section(self) -> list:
        """Build detailed diagnosis section"""
        elements = []
        
        elements.append(Paragraph("PROBLEM DIAGNOSIS", self.styles['Heading2']))
        elements.append(Spacer(1, 0.15*inch))
        
        for problem in self.diagnosis.problems_detected:
            # Problem heading with severity color
            severity_color = {'high': '#c41e3a', 'medium': '#ff8c00', 'low': '#4CAF50'}
            color = severity_color.get(problem.severity, '#000000')
            
            elements.append(Paragraph(
                f"<font color='{color}'><b>{problem.type.replace('_', ' ').title()}</b></font> "
                f"<font size='9'>({problem.severity.upper()}, {problem.confidence_percent}% confidence)</font>",
                self.styles['Heading3']
            ))
            
            # Evidence
            if problem.evidence:
                elements.append(Paragraph("<b>Evidence:</b>", self.styles['Normal']))
                for item in problem.evidence[:3]:
                    elements.append(Paragraph(f"• {item}", self.styles['Normal']))
            
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    # ========== RECOMMENDATIONS SECTION ==========
    def _build_recommendations_section(self) -> list:
        """Build recommendations section"""
        elements = []
        
        elements.append(Paragraph("RECOMMENDED ACTIONS", self.styles['Heading2']))
        elements.append(Spacer(1, 0.15*inch))
        
        rec_data = [["Priority", "Action", "Change", "Rationale"]]
        
        for rec in self.diagnosis.recommendations[:5]:  # Top 5 recommendations
            rec_data.append([
                str(rec.priority),
                rec.action.replace('_', ' ').title(),
                rec.delta,
                rec.rationale[:50] + "..." if len(rec.rationale) > 50 else rec.rationale
            ])
        
        rec_table = Table(rec_data, colWidths=[0.7*inch, 1.8*inch, 1*inch, 2.5*inch])
        rec_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ROWBACKGROUNDS', (0, 0), (-1, 0), [HexColor('#1f4788')]),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f0f0f0')]),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
        ]))
        
        elements.append(rec_table)
        
        # Setup delta summary
        if self.diagnosis.setup_delta:
            elements.append(Spacer(1, 0.15*inch))
            elements.append(Paragraph("<b>Setup Changes:</b>", self.styles['Normal']))
            
            delta = self.diagnosis.setup_delta
            changes = []
            if delta.rear_wing_angle_deg:
                changes.append(f"Rear Wing: {delta.rear_wing_angle_deg}")
            if delta.front_wing_angle_deg:
                changes.append(f"Front Wing: {delta.front_wing_angle_deg}")
            if delta.front_brake_bias_percent:
                changes.append(f"Brake Bias: {delta.front_brake_bias_percent}")
            if delta.traction_control_level:
                changes.append(f"Traction Control: {delta.traction_control_level}")
            
            for change in changes:
                elements.append(Paragraph(f"• {change}", self.styles['Normal']))
        
        return elements
    
    # ========== COACHING SECTION ==========
    def _build_coaching_section(self) -> list:
        """Build driver coaching section"""
        elements = []
        
        elements.append(Paragraph("DRIVER COACHING", self.styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        coaching = self.diagnosis.driver_coaching
        
        if coaching.braking_points:
            elements.append(Paragraph("<b>Braking Strategy:</b>", self.styles['Normal']))
            elements.append(Paragraph(coaching.braking_points, self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        if coaching.acceleration_strategy:
            elements.append(Paragraph("<b>Acceleration:</b>", self.styles['Normal']))
            elements.append(Paragraph(coaching.acceleration_strategy, self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        if coaching.line_adjustments:
            elements.append(Paragraph("<b>Line Adjustments:</b>", self.styles['Normal']))
            elements.append(Paragraph(coaching.line_adjustments, self.styles['Normal']))
        
        return elements
    
    # ========== FOOTER ==========
    def _build_footer(self) -> list:
        """Build footer section"""
        elements = []
        
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(
            "<hr color='#cccccc'/>",
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        footer_text = (
            "GT3 R Diagnostic Tool | Powered by Race Engineering Workstation Simulator (REWS)<br/>"
            f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}<br/>"
            "For professional use only. Consult with experienced engineers for race strategy."
        )
        elements.append(Paragraph(footer_text, self.styles['Normal']))
        
        return elements


# ========== CONVENIENCE FUNCTION ==========
def generate_report(
    diagnosis: DiagnosisResult,
    telemetry: ProcessedTelemetry,
    filename: str = "report.pdf"
) -> str:
    """Convenience function to generate PDF report"""
    generator = PDFGenerator(diagnosis, telemetry)
    return generator.generate(filename)