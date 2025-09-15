import re

# 线性插值函数
def lerp(c1, c2, t):
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * t)) for i in range(3))

# 生成色阶
def generate_shades(base_color):
    shades = {}
    white = (255, 255, 255)
    black = (0, 0, 0)

    shades[500] = base_color

    # 100–400: 朝白色插值
    for step, weight in zip([100, 200, 300, 400], [0.8, 0.6, 0.4, 0.2]):
        shades[step] = lerp(white, base_color, 1 - weight)

    # 600–900: 朝黑色插值
    for step, weight in zip([600, 700, 800, 900], [0.2, 0.4, 0.6, 0.8]):
        shades[step] = lerp(base_color, black, weight)

    return shades

# 解析 colors.css
def parse_colors(css_text):
    pattern = r'--color-([a-z]+): rgb\((\d+),\s*(\d+),\s*(\d+)\);'
    colors = re.findall(pattern, css_text)
    return {name: (int(r), int(g), int(b)) for name, r, g, b in colors}

# 写入 output.css
def write_output(light_color, dark_color, output_file="output.css"):
    with open(output_file, "w") as file:
        # Light scheme
        file.write("@media (prefers-color-scheme: light) {\n    :root {\n")
        for name, base in light_color.items():
            file.write(f"\n        /* {name} */\n")
            shades = generate_shades(base)
            for step in [100,200,300,400,500,600,700,800,900]:
                r, g, b = shades[step]
                file.write(f"        --color-{name}-{step}: rgb({r}, {g}, {b});\n")
        file.write("    }\n}\n\n")

        # Dark scheme
        file.write("@media (prefers-color-scheme: dark) {\n    :root {\n")
        for name, base in dark_color.items():
            file.write(f"\n        /* {name} */\n")
            shades = generate_shades(base)
            for step in [100,200,300,400,500,600,700,800,900]:
                r, g, b = shades[step]
                file.write(f"        --color-{name}-{step}: rgb({r}, {g}, {b});\n")
        file.write("    }\n}\n")

if __name__ == "__main__":
    with open("colors.css", "r") as f:
        css = f.read()

    light_block = re.search(r'@media \(prefers-color-scheme: light\)\s*{([^}]*)}', css, re.S).group(1)
    dark_block = re.search(r'@media \(prefers-color-scheme: dark\)\s*{([^}]*)}', css, re.S).group(1)

    light_colors = parse_colors(light_block)
    dark_colors = parse_colors(dark_block)

    write_output(light_colors, dark_colors)
    print("已生成 output.css，每个色块已分开。")
