from fakts.fakts import Fakts
from fakts.fakts import Fakts
from typing import Optional
from fakts.grants.remote.discovery.well_known import WellKnownDiscovery
from fakts.grants.remote import RemoteGrant
from fakts.grants.remote.demanders.auto_save import AutoSaveDemander
from fakts.grants.remote.demanders.cache import CacheTokenStore
from fakts.grants.remote.demanders.static import StaticDemander
from fakts.grants.remote.demanders.device_code import DeviceCodeDemander
from fakts.grants.remote.claimers.post import ClaimEndpointClaimer
from fakts.grants.remote.demanders.redeem import RedeemDemander
from arkitekt_next_next.model import Manifest


class ArkitektNextFaktsQt(Fakts):
    grant: RemoteGrant


class ArkitektNextFakts(Fakts):
    pass


def build_arkitekt_next_fakts(
    manifest: Manifest,
    url: Optional[str] = None,
    no_cache: bool = False,
    headless: bool = False,
) -> ArkitektNextFakts:
    identifier = manifest.identifier
    version = manifest.version

    if no_cache:
        demander = DeviceCodeDemander(
            manifest=manifest,
            redirect_uri="http://127.0.0.1:6767",
            open_browser=not headless,
        )

    else:
        demander = AutoSaveDemander(
            demander=DeviceCodeDemander(
                manifest=manifest,
                redirect_uri="http://127.0.0.1:6767",
                open_browser=not headless,
            ),
            store=CacheTokenStore(
                cache_file=f".arkitekt_next/cache/{identifier}-{version}_fakts_cache.json"
            ),
        )

    return ArkitektNextFakts(
        grant=RemoteGrant(
            demander=demander,
            discovery=WellKnownDiscovery(url=url, auto_protocols=["https", "http"]),
            claimer=ClaimEndpointClaimer(),
        )
    )


def build_arkitekt_next_token_fakts(
    manifest: Manifest,
    token: str,
    url,
    no_cache: Optional[bool] = False,
    headless=False,
):
    return ArkitektNextFakts(
        grant=RemoteGrant(
            demander=StaticDemander(token=token),
            discovery=WellKnownDiscovery(url=url, auto_protocols=["https", "http"]),
            claimer=ClaimEndpointClaimer(),
        )
    )

def build_arkitekt_next_redeem_fakts(
    manifest: Manifest,
    redeem_token: str,
    url,
    no_cache: Optional[bool] = False,
    headless=False,
):
    return ArkitektNextFakts(
        grant=RemoteGrant(
            demander=RedeemDemander(token=redeem_token, manifest=manifest),
            discovery=WellKnownDiscovery(url=url, auto_protocols=["https", "http"]),
            claimer=ClaimEndpointClaimer(),
        )
    )
