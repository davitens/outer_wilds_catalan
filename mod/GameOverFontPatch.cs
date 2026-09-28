using HarmonyLib;
using UnityEngine;

namespace CatalanTranslation
{
    // Interplanetary Polyglot patches every font accessor except GetGameOverFont,
    // so a custom language index overflows the game's per-language font array.
    // Fall back to the active language font for any non-vanilla language.
    [HarmonyPatch(typeof(TextTranslation), nameof(TextTranslation.GetGameOverFont))]
    internal static class GameOverFontPatch
    {
        [HarmonyPrefix]
        private static bool Prefix(ref Font __result)
        {
            try
            {
                var language = (int)TextTranslation.Get().GetLanguage();
                if (language < 0 || language > (int)TextTranslation.Language.TOTAL)
                {
                    __result = TextTranslation.GetFont(false);
                    return false;
                }
            }
            catch
            {
                // fall through to the original method
            }

            return true;
        }
    }
}
