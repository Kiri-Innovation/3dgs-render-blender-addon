vec4 blender_srgb_to_framebuffer_space(vec4 in_color)
{
  vec3 c = max(in_color.rgb, vec3(0.0));
  vec3 c1 = c * (1.0 / 12.92);
  vec3 c2 = pow((c + 0.055) * (1.0 / 1.055), vec3(2.4));
  in_color.rgb = mix(c1, c2, step(vec3(0.04045), c));
  return in_color;
}

void main()
{
  vec4 texColor = texture(image, uvInterp);
  FragColor = blender_srgb_to_framebuffer_space(texColor);
}