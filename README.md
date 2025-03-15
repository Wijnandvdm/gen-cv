# GenCV
First things first, congratulations for actually reading a README!

Secondly, since Word continues its assault on nicely formatted pages in Curriculum Vitaes, with this repository you are able to generate your very own nicely formatted CV in PDF format. Also, I've tried LaTeX a little bit, not my jazz. But if it is for you, great!

## Schematic overview
![](./docs/schematic_overview.drawio.png)

## How it works
1. **Template Setup**:
   - Copy the `wijnand_van_der_meijs.yaml` file.
   - Paste it in the same folder and rename it to `<your_name>.yaml`.

2. **Customization**:
   - Fill in the YAML file with your details.
   - *(Optional)* Modify hex color codes in the YAML to match your preferences.
   - Replace `profile_picture.png` with your own picture, ensuring the filename remains `profile_picture.png`.

3. **CV Generation**:
   - Run the script with `poetry run python gen-cv.py <your_name>`.
   - Your personalized CV will be generated as a nicely formatted PDF!

This of course does not explain the complete functionality of this project. Want to know more? Don't be shy, ask the creator of this repo!