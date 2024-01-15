import json
import argparse

from ngii2lanelet import NGII2LANELET


def main(args):
    lanelet = NGII2LANELET(
        folder_path=args.ngii_path,
        precision=args.precision,
        base_lla=args.base_lla,
        is_utm=args.is_utm
        )

    name = args.ngii_path.split('/')[-1]

    with open('%s.json'%(name), 'w', encoding='utf-8') as f:
        json.dump(lanelet.map_data, f, indent="\t")

    with open('%s_ID.json'%(name), 'w', encoding='utf-8') as f:
        json.dump(lanelet.link_id_data, f, indent="\t")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    name = 'KCity'

    parser.add_argument('--ngii_path', type=str, default='./%s'%(name))
    parser.add_argument('--precision', type=float, default=0.5)
    parser.add_argument('--base_lla', type=tuple, default=(37.2292221592864, 126.76912499027308, 29.18400001525879), help='(lat, lon, alt)')
    parser.add_argument('--is_utm', type=bool, default=True)

    args = parser.parse_args()

    main(args)

    #** KCity 37.2292221592864, 126.76912499027308, 29.18400001525879 utm True L_LinkID
    # songdo 37.39657805498484, 126.6321430873685,7.369
    #** songdo-epitone 37.3888319, 126.6428739, 7.369 utm False L_LinKID
    # songdo-testbed 37.4179788, 126.6140342, 7
    # songdo-campus 37.383378, 126.656798, 7
    # fmtc 37.3656136, 126.7251893, 31.8