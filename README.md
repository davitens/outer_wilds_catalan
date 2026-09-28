![Banner](banner.png)

# Traducció al català d'Outer Wilds

Mod que tradueix **Outer Wilds** completament al català, fet amb
[OWML](https://outerwildsmods.com/) i
[Interplanetary Polyglot](https://github.com/xen-42/outer-wilds-localization-utility).
No modifica els fitxers del joc: tot s'instal·la com un mod a `OWML/Mods/`.

## Requisits

- Outer Wilds (versió 1.1.16.1372 o compatible)
- [Outer Wilds Mod Manager](https://outerwildsmods.com/mod-manager/). En obrir-lo per
  primera vegada et demanarà d'instal·lar
  **[OWML](https://outerwildsmods.com/mods/owml/)**; accepta i deixa que el faci servir.
- El mod **Interplanetary Polyglot** (`xen.LocalizationUtility`), que aporta el suport
  d'idiomes. Es pot instal·lar des del mateix gestor.

## Instal·lació

Aquest mod **encara no és al repositori oficial de mods**, així que de moment només es
pot instal·lar manualment:

1. Obre el **Outer Wilds Mod Manager** i instal·la
   **[OWML](https://outerwildsmods.com/mods/owml/)** quan te'l demani. Després instal·la
   **Interplanetary Polyglot** des de la pestanya *Mods*.
2. Descarrega el `.zip` del mod des de la pestanya **Releases** d'aquest repositori.
3. Descomprimeix-lo dins la carpeta `OWML/Mods/`, de manera que quedi així:

   ```
   OWML/Mods/davitens.CatalanTranslation/
     manifest.json
     CatalanTranslation.dll
     assets/Translation.xml
   ```

   La carpeta `OWML/Mods/` és dins la instal·lació del joc, per exemple
   `C:\Program Files (x86)\Steam\steamapps\common\Outer Wilds\OWML\Mods\` (Steam) o la
   carpeta equivalent d'Epic.
4. Inicia el joc des del gestor.

## Activar el català

Al joc: **Opcions → Idioma → Català**.

## Estat

- Traducció completa: interfície, registre de bord i diàlegs.
- Qualsevol cadena sense traduir es mostra en anglès.

## Crèdits i avís legal

- Traducció: [davitens](https://github.com/davitens)
- Interplanetary Polyglot: xen-42
- Outer Wilds és propietat de Mobius Digital. Aquest és contingut fet per fans i
  segueix la
  [política de contingut de fans](https://www.mobiusdigitalgames.com/fan-content-policy.html).

## Llicència

[MIT](LICENSE).

## English

A full Catalan translation mod for **Outer Wilds**, built on
[OWML](https://outerwildsmods.com/) and
[Interplanetary Polyglot](https://github.com/xen-42/outer-wilds-localization-utility).
It never touches the game files; everything ships as an OWML mod.

**Install:** this mod is not on the official mod repository yet, so it must be
installed manually for now. Open the
[Outer Wilds Mod Manager](https://outerwildsmods.com/mod-manager/) and let it install
[OWML](https://outerwildsmods.com/mods/owml/) when prompted; install
**Interplanetary Polyglot** from the *Mods* tab; then download the mod's `.zip` from
the **Releases** tab of this repo and extract it into the game's `OWML/Mods/` folder,
so you get `OWML/Mods/davitens.CatalanTranslation/`. Launch the game from the manager
and set **Options → Language → Català**. Untranslated strings fall back to English.
Licensed under MIT; fan content per Mobius Digital's fan content policy.
