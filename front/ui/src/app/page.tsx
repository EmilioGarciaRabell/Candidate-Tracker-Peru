import Image from "next/image";
import Link from "next/link";
import styles from "./home.module.css"; 

export default function Home() {
  return (
    <section className={styles.background}>
      <div className={styles.padding}>

        <div className={styles.home}>

          <div>

            <h1 className="text-base font-semibold tracking-wider text-blue-600 uppercase"> Por un Peru informado en miras a las elecciones 2026</h1>

            <p className="mt-4 text-4xl font-bold text-black lg:mt-8 sm:text-6xl xl:text-8xl">Informate por un Peru mejor</p>

              <Link href="/candidates">
                <button className="mt-10 px-5 py-2.5 text-base transition-all duration-200 hover:bg-red-400 hover:text-black focus:text-black focus:bg-yellow-400 font-semibold text-white bg-black rounded-full">
                  Infórmate ahora
                </button>
              </Link>

          </div>

          <div className={styles.imageSection}>
            <Image
              src="/landing.svg"
              alt="imagen del landing page"
              width={100}
              height={100}
              className="w-full rounded-4xl"
            />
          </div>

        </div>
          

      </div>
    </section>
  );
}
