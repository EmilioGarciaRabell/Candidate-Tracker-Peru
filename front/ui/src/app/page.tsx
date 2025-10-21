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
                <button className="customButton mt-10">
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
