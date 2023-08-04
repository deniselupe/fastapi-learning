export default function HomePage() {
  return (
    <main>
      <form
        className="w-2/6 h-3/4 min-w-[400px] mx-auto mt-28 p-10 rounded-3xl flex flex-col items-center shadow-xl"
        action="http://localhost:8000/login"
        method="post"
      >
        <div className="w-full mb-4">
          <h1 className="mb-2 text-5xl text-center text-yellow-500">Welcome back!</h1>
          <h2 className="text-center text-yellow-500">We are so excited to see you again!</h2>
        </div>
        <div className="w-full mb-4">
          <label className="mb-2 text-2xl block text-yellow-500" htmlFor="firstname">First Name:</label>
          <input className="w-full block text-1xl leading-8 rounded" type="text" name="firstname" id="firstname" />
        </div>
        <div className="w-full mb-4">
          <label className="mb-2 text-2xl block text-yellow-500" htmlFor="lastname">Last Name:</label>
          <input className="w-full block text-1xl leading-8 rounded" type="text" name="lastname" id="lastname" />
        </div>
        <div className="w-full mb-12">
          <label className="mb-2 text-2xl block text-yellow-500" htmlFor="age">Age:</label>
          <input className="w-full block text-1xl leading-8 rounded" type="number" name="age" id="age" />
        </div>
        <button type="submit" className="w-full mb-4 text-2xl rounded bg-yellow-500 hover:bg-cyan-400">Submit</button>
      </form>
    </main>
  );
}
