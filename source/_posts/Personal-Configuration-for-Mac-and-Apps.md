---
title: Personal Configuration for Mac and Apps
date: 2017-01-30 12:41:00
categories: Configuration
tags: [Mac, Config]
description:
---

**Continue Updating**

Here are my configurations and settings for mac and apps in order to reach a higher productivity. Some config files can be found in the following repo: [https://github.com/hippo-jessy/MacAndAppsConfig](https://github.com/hippo-jessy/MacAndAppsConfig)

## Current Environments

OS: Mac OS X EI Capitan(version 10.11.6)

## Useful Apps and Tools for Mac

- **Karabiner && Seil**

  - **Karabiner:**

    This app can be used to remap keyboard and shortcut. I take use of it to remap "ctrl+k/j/h/l" to Arrow keys(Up/Down/Left/Right). My personal config file is right here: [https://github.com/hippo-jessy/MacAndAppsConfig/blob/master/Karabiner/private.xml](https://github.com/hippo-jessy/MacAndAppsConfig/blob/master/Karabiner/private.xml)

  - **Seil:**

    I use this app only for its functionality to remap Caps Lock to esc. It's pretty much helpful when editing in vim mode. Although most remapping actions can be perfomed by Karabiner, it can do nothing with this special key(Karabiner is currently working to support MacOS Sierra and trying to fully integrate Seil, you can [check it here]([https://github.com/tekezo/Karabiner-Elements](https://github.com/tekezo/Karabiner-Elements))).

- **iStat Menus**

  This one is basically a profiling tool which show dynamic status of CPU, memory, disks, etc. All these information is presented in the menubar and in a pleasant way as the following picture shown:

  ![ Personal Configuration for Mac and Apps](http://ojnnon64z.bkt.clouddn.com/Personal Configuration for Mac and Apps.png)

## Keyboard and Shortcut Remapping

- **Disable shortcut CMD+H systemwide "hide window" functionality and reassign it to different action in specific apps**. No additional tool is needed to fulfil this remapping process and try to follow these steps:

  1. Go to *System Preference* and locate *KeyBoard*

  2. Go to *Keyboard Shortcuts* sub tab at the top 

  3. Choose *App Shortcuts* on the list at left side

  4. Click on the + sign below the list to the right

  5. See the following screenshot, where I've reassigned CMD+H  to "left with selection" action in IntelliJ IDEA exclusively.

     *Tips: choose "All controls" for pressing Tab could also fast your keyboard operation.*

     ![Personal Configuration for Mac and Apps_1](http://ojnnon64z.bkt.clouddn.com/Personal Configuration for Mac and Apps_1.png)

- **Remap Ctrl + H/J/K/L to Arrow keys(left/down/up/right) **considering anti human location of Arrow keys. Take good use of **Karabiner** to achieve this task as I mentioned before. 

- **Remap caps lock to esc** using **Seil** to speed up vim mode editing.

- **Remember to switch Mac Function Keys(such as F1, F2) to standard function keys** in that many apps like browsers, IDEs may take these keys as part of shortcuts.

## Settings for IntelliJ IDEA

I changed most of keymap settings of IntelliJ IDEA based on my own habits and most of these changed shortcuts are easier to remember. You can find the settings file here: [settings exported](https://github.com/hippo-jessy/MacAndAppsConfig/tree/master/IntelliJ_IDEA)


**To Be Continued …**