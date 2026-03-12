void main()
{
    vec2 screen_coord = gl_FragCoord.xy / depth_texture_size;
    float sampled_depth = texture(blender_depth, screen_coord).r;
    
    if (v_depth > sampled_depth) {
        discard;
    }
    
    float power = -0.5 * (v_conic.x * v_coordxy.x * v_coordxy.x + v_conic.z * v_coordxy.y * v_coordxy.y) - v_conic.y * v_coordxy.x * v_coordxy.y;
    if (power > 0.0)
        discard;
    float opacity = min(0.99, v_alpha * exp(power));
    if (opacity < 0.00392)
        discard;
    if (v_render_mode == 2) {
        fragColor = vec4(v_color, 1.0);
        return;
    }

    fragColor = vec4(v_color, opacity);
}