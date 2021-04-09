# /bin/python3
import os
import sys
import argparse


class BaseThrow(dict):
  name: str
  stat: str
  subtitle: str

  def __init__(self, name: str, stat: str, **kwargs):
    self.name = name
    self.stat = stat
    self.subtitle = stat.capitalize()

    for key, value in kwargs.items():
      setattr(self, key, value)

  def __getattr__(self, attr):
    return self[attr]


class GenericThrow(BaseThrow):
  def __init__(self, name: str, stat: str, type="number", **kwargs):
    super().__init__(name,
                     stat,
                     **kwargs,
                     type=type,
                     roll=f"{name.capitalize()} save: {{1d20 + {name}}}")

  def __str__(self):
    return f'Save {self.name} ({self.stat.capitalize()})'


class SaveThrow(BaseThrow):
  def __init__(self, name: str, stat: str, **kwargs):
    super().__init__(name,
                     stat,
                     type="save-throw",
                     section="save-throws",
                     value=0,
                     roll=f"{name.capitalize()} save: {{1d20 + {name}}}", **kwargs)

  def __str__(self):
    return f'Save {self.name} ({self.stat.capitalize()})'


class SkillThrow(BaseThrow):
  def __init__(self, name: str, stat: str, **kwargs):
    super().__init__(name,
                     stat,
                     type="skill",
                     section="skills",
                     value=0,
                     roll=f"{name.capitalize()} roll: {{1d20 + {name}}}", **kwargs)

  def __str__(self):
    return f'Talent {self.name} ({self.stat.capitalize()})'


def generateTemplate(inpt, outpt, **kwargs):
  import jinja2
  tm = jinja2.Template(inpt.read())
  rendered = tm.render(**kwargs)
  outpt.write(rendered)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t",
                      "--template",
                      default=os.path.join(os.path.dirname(__file__),
                                           "templates/charactersheet_pj.j2"),
                      help="Template file to use as input",
                      type=argparse.FileType("r"))
  parser.add_argument("-o",
                      "--output",
                      default=sys.stdout,
                      help="File to use as output (default to stdout)",
                      type=argparse.FileType("w"))
  args = parser.parse_args()
  throwList = [
      SaveThrow("fortitude", "con"),
      SaveThrow("reflex", "dex"),
      SaveThrow("will", "wis"),
      GenericThrow("perception", "wis", type="number", section="perception"),

      SkillThrow("acrobatics", "dex", is_armor_dependant=True),
      SkillThrow("arcana", "int"),
      SkillThrow("athletics", "str", is_armor_dependant=True),
      SkillThrow("crafting", "int"),
      SkillThrow("deception", "cha"),
      SkillThrow("diplomacy", "cha"),
      SkillThrow("intimidation", "cha"),
      SkillThrow("medicine", "wis"),
      SkillThrow("nature", "wis"),
      SkillThrow("occultism", "int"),
      SkillThrow("performance", "cha"),
      SkillThrow("religion", "wis"),
      SkillThrow("society", "int"),
      SkillThrow("stealth", "dex", is_armor_dependant=True),
      SkillThrow("survival", "wis"),
      SkillThrow("thievery", "dex", is_armor_dependant=True),
      SkillThrow("a-lore", "int"),
      SkillThrow("b-lore", "int"),
  ]
  blacklisted_keys = ["name", "is_armor_dependant"]

  throws = [t.__dict__ for t in throwList]

  generateTemplate(args.template, args.output, throws=throws, blacklisted_keys=blacklisted_keys)
