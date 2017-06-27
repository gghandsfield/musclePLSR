
gfx read nodes init_gas time 0
gfx read elements init_gas
gfx read nodes def_gas time 1

gfx read nodes /home/jfer004/DTI_muscle_contraction/bones/femur
gfx read elements /home/jfer004/DTI_muscle_contraction/bones/femur

gfx read nodes /home/jfer004/DTI_muscle_contraction/bones/tibia
gfx read elements /home/jfer004/DTI_muscle_contraction/bones/tibia

gfx modify g_element femur general clear circle_discretization 6 default_coordinate coordinates element_discretization "4*4*4" native_discretization none;
gfx modify g_element femur lines select_on invisible material default selected_material default_selected;
gfx modify g_element femur surfaces select_on material bone selected_material default_selected render_shaded;
gfx modify g_element tibia general clear circle_discretization 6 default_coordinate coordinates element_discretization "4*4*4" native_discretization none;
gfx modify g_element tibia lines select_on invisible material default selected_material default_selected;
gfx modify g_element tibia surfaces select_on material bone selected_material default_selected render_shaded;

gfx create window 1 double_buffer;
gfx modify window 1 image scene default light_model default;
gfx modify window 1 image add_light default;
gfx modify window 1 layout simple ortho_axes z -y eye_spacing 0.25 width 512 height 512;
gfx modify window 1 set current_pane 1;
gfx modify window 1 background colour 0 0 0 texture none;
gfx modify window 1 view parallel eye_point 21.3467 934.155 371.753 interest_point 93.9858 126.475 346.701 up_vector 0.0649643 -0.0250986 0.997572 view_angle 38.2025 near_clipping_plane 8.11326 far_clipping_plane 2899.4 relative_viewport ndc_placement -1 1 2 2 viewport_coordinates 0 0 1 1;
gfx modify window 1 overlay scene none;
gfx modify window 1 set transform_tool current_pane 1 std_view_angle 40 normal_lines no_antialias depth_of_field 0.0 fast_transparency blend_normal;

for($i=0.1;$i<1.1;$i=$i+0.4)
{
  for($j=0.1;$j<1.1;$j=$j+0.4)
  {
    for($k=0.1;$k<1.1;$k=$k+0.4)
    {
     gfx mod g_element gas streamlines cylinder vector fibres length 100 material muscle xi $i $j $k 
    }
  }
}