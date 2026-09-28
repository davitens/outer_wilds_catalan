using HarmonyLib;
using OWML.Common;
using OWML.ModHelper;
using System.Reflection;

namespace CatalanTranslation
{
    public class CatalanTranslation : ModBehaviour
    {
        private void Start()
        {
            try
            {
                Harmony.CreateAndPatchAll(Assembly.GetExecutingAssembly(), "davitens.CatalanTranslation");
            }
            catch (System.Exception e)
            {
                ModHelper.Console.WriteLine($"Failed to apply font patch: {e}", MessageType.Warning);
            }

            var api = ModHelper.Interaction.TryGetModApi<ILocalizationAPI>("xen.LocalizationUtility");
            if (api == null)
            {
                ModHelper.Console.WriteLine("Could not find xen.LocalizationUtility (Interplanetary Polyglot).", MessageType.Error);
                return;
            }

            api.RegisterLanguage(this, "Catalan", "assets/Translation.xml");
            ModHelper.Console.WriteLine("Catalan translation loaded.", MessageType.Success);
        }
    }
}
